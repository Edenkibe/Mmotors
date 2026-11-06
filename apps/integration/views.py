from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.dossiers.models import DossierAchat
from apps.location.models import DossierLocation
from apps.core.yousignservice import YousignClient
from django.core.files.base import ContentFile
import json
import logging
from apps.voiture.service import invoice,invoice_location
from django.http import HttpResponse
from django.conf import settings
import stripe
from django.db import transaction
from django.utils import timezone
from apps.location.models import payementLocation
stripe.api_key = settings.STRIPE_SECRET_KEY
from decimal import Decimal
import hmac
import hashlib
import json
logger = logging.getLogger(__name__)

#webhook yousigh  for achat and location together we are combining both in one webhook:
@csrf_exempt
def yousign_webhook(request):
    
    print(" YOUSIGN WEBHOOK ENTERED ", flush=True)

    logger.info("YOUSIGN WEBHOOK ENTERED ")

 
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )
    # =========================================
    # 1. GET WEBHOOK SECRET
    # =========================================

    secret = settings.YOUSIGN_WEBHOOK_SECRET

    if not secret:
        logger.error("Yousign webhook secret is missing")

        return JsonResponse(
            {"error": "Webhook secret not configured"},
            status=500
        )

    # =========================================
    # 2. GET SIGNATURE FROM YOUSIGN HEADER
    # =========================================

    received_signature = request.headers.get(
        "x-yousign-signature-256",
        ""
    )

    # =========================================
    # 3. CALCULATE EXPECTED SIGNATURE
    # =========================================

    expected_signature = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        request.body,
        hashlib.sha256
    ).hexdigest()

    # =========================================
    # 4. VERIFY WEBHOOK AUTHENTICITY
    # =========================================

    if not received_signature or not hmac.compare_digest(
        received_signature,
        expected_signature
    ):

        logger.warning("Invalid Yousign webhook signature")

        return JsonResponse(
            {"error": "Invalid webhook signature"},
            status=401
        )

    logger.info("Yousign webhook signature verified")

    # =========================================
    # 5. READ JSON ONLY AFTER VERIFICATION
    # =========================================
    try:
        data = json.loads(request.body)

        logger.info("Yousign webhook received: %s", data)

        # We only process completed signature requests
        if data.get("event_name") != "signature_request.done":
            return JsonResponse({
                "ok": True,
                "ignored": True
            })

        # Get signature request
        signature_request = data["data"]["signature_request"]

        request_id = signature_request["id"]
        external_id = signature_request.get("external_id")

        logger.info(
            "Yousign signature done - request_id=%s external_id=%s",
            request_id,
            external_id
        )

        if not external_id:
            logger.error("Yousign webhook: missing external_id")

            return JsonResponse(
                {"error": "Missing external_id"},
                status=400
            )

        client = YousignClient()
     
        # ACHAT:
        if external_id.startswith("achat-"):

            achat_id = external_id.replace("achat-", "", 1)

            try:
                demande = DossierAchat.objects.get(
                    id=achat_id
                )
            except DossierAchat.DoesNotExist:

                logger.error(
                    "Achat not found: %s",
                    achat_id
                )

                return JsonResponse(
                    {"error": "Achat not found"},
                    status=404
                )


            # Download signed PDF
            pdf = client.download_signed_document(
                request_id
            )


            # Save signed PDF
            demande.signed_contract_pdf.save(
                f"signed_contract_{demande.id}.pdf",
                ContentFile(pdf),
                save=False
            )

            # Update status
            demande.mysignature = "signé"
            demande.save()
            logger.info(
                "Achat %s successfully signed",
                demande.id
            )


       
        # LOCATION:
        elif external_id.startswith("location-"):

            location_id = external_id.replace("location-","",1)
            try:
                demande = DossierLocation.objects.get(
                    id=location_id
                )
            except DossierLocation.DoesNotExist:

                logger.error(
                    "Location not found: %s",
                    location_id
                )

                return JsonResponse(
                    {"error": "Location not found"},
                    status=404
                )


            # Download signed PDF
            pdf = client.download_signed_document(
                request_id
            )


            # Save signed PDF
            demande.signed_contract_pdf.save(
                f"signed_contract_{demande.id}.pdf",
                ContentFile(pdf),
                save=False
            )

            # Update status
            demande.mysignature = "signé"
            demande.save()

            logger.info(
                "Location %s successfully signed",
                demande.id
            )

        else:

            logger.error(
                "Unknown Yousign external_id: %s",
                external_id
            )

            return JsonResponse(
                {
                    "error": "Unknown external_id",
                    "external_id": external_id
                },
                status=400
            )


        return JsonResponse({
            "ok": True
        })


    except json.JSONDecodeError:

        logger.exception(
            "Invalid JSON received from Yousign"
        )

        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )


    except Exception as e:

        logger.exception(
            "Yousign webhook failed"
        )

        return JsonResponse(
            {"error": str(e)},
            status=500
        )
        
        
        
# strpe webhook for location and achat:
@csrf_exempt
def stripe_webhook(request):

    payload = request.body

    sig_header = request.META.get(
        "HTTP_STRIPE_SIGNATURE"
    )

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

    except Exception as e:
        return HttpResponse(
            str(e),
            status=400
        )


    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        metadata = session.metadata

        payment_type = metadata["type"]

        print(payment_type)
        
        if session["currency"] != "eur":
            return HttpResponse(status=400)
  
        # ACHAT    
        if payment_type == "achat":

            achat_id = metadata["achat_id"]
            try:
                achat_dossier = DossierAchat.objects.get(
                    id=achat_id
                )

            except DossierAchat.DoesNotExist:
                return HttpResponse(
                    "Achat not found",
                    status=404
                )


            expected_amount = int(
                achat_dossier.vehicule.prix * 100
            )


            if session["amount_total"] != expected_amount:
                return HttpResponse(
                    "Wrong amount",
                    status=400
                )


            created = False

            with transaction.atomic():

                if achat_dossier.deal != "acheté":

                    achat_dossier.deal = "acheté"
                    achat_dossier.stripe_session_id = session.id
                    achat_dossier.stripe_payment_intent = session.payment_intent
                    achat_dossier.stripe_customer_id = session.customer
                    achat_dossier.paid_amount = Decimal(session.amount_total) / Decimal("100")
                    achat_dossier.paid_currency = session.currency
                    achat_dossier.paid_at = timezone.now()

                    achat_dossier.save()
                    # make car unavailable
                    vehicule = achat_dossier.vehicule
                    vehicule.disponibilite = "acheté"
                    vehicule.save()


                    created = True


            if created:
                invoice(achat_dossier)


        # LOCATION
        elif payment_type == "location":

            location_id = metadata["location_id"]

            try:
                location_dossier = DossierLocation.objects.get(
                    id=location_id
                )
                

            except DossierLocation.DoesNotExist:
                return HttpResponse(
                    "Location not found",
                    status=404
                )

            days = (
                location_dossier.date_retour
                - location_dossier.date_depart
            ).days
             
            payer= location_dossier.vehicule.prix * days
            expected_amount = int(
                location_dossier.vehicule.prix * days * 100
            )

            if session.amount_total != expected_amount:
                return HttpResponse(
                    "Wrong amount",
                    status=400
            )

            with transaction.atomic():

                if location_dossier.deal != "en location":

                    location_dossier.deal = "en location"

                    location_dossier.save()


                    # Store Stripe info in your separate model
                created = payementLocation.objects.update_or_create(
                    location=location_dossier,
                    defaults={
                        "stripe_session_id": session.id,
                        "stripe_payment_intent": session.payment_intent,
                        "stripe_customer_id": session.customer,                      
                        "paid_amount":Decimal(session.amount_total) / Decimal("100"),
                        "paid_currency": session.currency,
                        "paid": True,
                    }
                )
            if created :
                invoice_location(location_dossier,payer,days)    
              
        else:

            return HttpResponse(
                "Unknown payment type",
                status=400
            )

    return HttpResponse(status=200)