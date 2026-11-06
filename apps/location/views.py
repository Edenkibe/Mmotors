from django.shortcuts import get_object_or_404, redirect, render
from apps.location.forms.LocationForm import DossierLocationForm 
from apps.location.forms.repondre_locationForm import Reply_locatioForm
from .models import DossierLocation
from apps.dossiers.models import DossierAchat
from apps.voiture.models import Voiture
from apps.core.yousignservice import YousignClient
from django.contrib import messages
import logging
from django.db.models import Q
logger = logging.getLogger(__name__)
from apps.location.models import payementLocation
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http import HttpResponse
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from datetime import date, datetime

def creer_dossier_location(request, id):
    voiture = get_object_or_404(Voiture, id=id)

    #if this exist in the dossier we shall show a text to the user that he already demanding this car:
    dossier_exist=DossierLocation.objects.filter(
        vehicule=voiture,
        status__in=['accepté','rejeté'],
        client=request.user,
        mysignature='not yet',
        deal=['disponible']
        ).exists()
    count=DossierLocation.objects.filter(vehicule=voiture,status__in=['encours', 'accepté']).count()
    if request.method == "POST":
        form = DossierLocationForm(request.POST)

        if form.is_valid():
            date_depart = form.cleaned_data['date_depart']
            date_retour = form.cleaned_data['date_retour']

            # Calculate booking days
            days = (date_retour - date_depart).days
            if days <= 0:
                return render(request, "faile_request_location.html",{'voiture': voiture}, status=400)
            
            dossier = form.save(commit=False)
            dossier.client = request.user
            dossier.vehicule = voiture
            dossier.save()

            return redirect("locations:user_satisfaction_location", id=dossier.id)

    else:
        form = DossierLocationForm()

    return render(request, "depot_location.html", {
        "form": form,
        "voiture": voiture,
        'dossier_exist': dossier_exist,
        'count': count
    })

#recuperer la voiture pour la location: demander a l'utilisateur si il est d accord avec le prix de la location et le nombre de jours de location: 
def user_satisfaction_location(request, id):
    
    dossier = get_object_or_404(DossierLocation, id=id, client=request.user) 
    days = (dossier.date_retour - dossier.date_depart).days
    
    # la datte de retour doit être après la date de début, sinon on retourne une erreur: pour 1 jour 
    
    total_price = dossier.vehicule.prix * days 
    context={
        'dossier': dossier,
        'days': days,
        'total_price': total_price
     }
    return render(request, "user_satisfaction_location.html", context)

# effacer le dossier location si l'utilisateur n'est pas satisfait du prix de la location ou du nombre de jours de location:
def user_not_satisfied_location(request, id):
    dossier = get_object_or_404(DossierLocation, id=id, client=request.user) 
    dossier.delete()
    return redirect("locations:unsuccess_location")


def unsuccess_location(request):
    return render(request, "unsuccess_location.html") 


# success de location: when the user submit the form of location we redirect him to this page:
def success_location(request):
    return render(request, "success_location.html")  

# view rejected booking in notification:user action
def rejected_location(request, id):
    
    
    #fetch the notification for the user  for the accepted or rejected demand in book mode:
    
    notification=DossierLocation.objects.filter(client=request.user,status__in=['accepté','rejeté'],mysignature='not yet')
    count_notification=notification.count()
    #getting the demandes:
    demande=get_object_or_404(DossierLocation,id=id,status='rejeté',mysignature='not yet')
    
    #when we click on this page we have to remove the notification by changing msignaturer not yet to signé:
    demande.mysignature="signé"
    demande.save()
    
    context={
        'demande':demande,
        'notification':notification,
        'count_notification': count_notification
    }
    return render(request,'rejected_location.html',context)  


#admin getting all demand booking on the dashboard
def get_demande_location(request):
    
    # all achat demande pending for the admin:
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #getting all pending demande  location for the admin and count them:
    dossier_location=DossierLocation.objects.filter(status ="encours")
    count_location=dossier_location.count()
    
    #count all demande booking in the system:
    all_demandes=DossierLocation.objects.all().order_by('-id')
    count_all_demandes=all_demandes.count()
    
    #all  demande en location in the system:ou en location running:
    all_sold=DossierLocation.objects.filter(status="en location")
    count_all_sold=all_sold.count()
    
    #get all booking car:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    context={
        'dossier':dossier,
        'count':count,
        'dossier_location':dossier_location,
        'count_location':count_location,
        'count_all_demandes':count_all_demandes,
        "all_demandes":all_demandes,
        'count_all_sold':count_all_sold,
    }
    return render(request,"administration/new_booking.html",context)


#the admin search location demande by it unique code::
def search_location(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne tout le user
    if query == "":
        dossier_user = DossierLocation.objects.filter().all()

    elif len(query) >= 2:
        filters = (
            Q(code_location__icontains=query)
        )

        dossier_user = DossierLocation.objects.filter(filters).all()

    else:
        dossier_user = DossierLocation.objects.none()

    context = {
        "query": query,
        "dossier_user": dossier_user,
        "total": dossier_user.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "administration/ajax/location_ajax.html",
            context,
        )

#repondre a une demande de location:
def repondre_location(request,id):
    
    #getting all pending demande d achat et location for the admin and count them:
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all booking car en pendind de validation:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
        
    #admin is getting  a demande to reply to it:
    demandes=get_object_or_404(DossierLocation,id=id)
    
    if request.method == "POST":
        
        # Keep the status BEFORE saving the form
        old_status = demandes.status

        form = Reply_locatioForm(
            request.POST,
            instance=demandes
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # Save the form
                    demandes = form.save()

                    # Status AFTER saving the form
                    new_status = demandes.status

                    # Only create/send Yousign when the status
                    # changes to "accepte"
                    if new_status == "accepté" and old_status != "accepté":

                        client = YousignClient()

                        # 1. Create the PDF contract
                        client.generate_contract(
                            demandes,
                            "location"
                        )

                        # 2. Create Yousign signature request
                        signature_request = client.create_signature_request(
                            demandes,
                            "location"
                        )

                        demandes.yousign_request_id = (
                            signature_request["id"]
                        )

                        # 3. Upload the contract PDF
                        document = client.upload_document(
                            signature_request["id"],
                            demandes.contrat_pdf.path
                        )

                        # 4. Save Yousign document ID
                        demandes.yousign_document_id = (
                            document["id"]
                        )

                        # 5. Add the client as signer
                        client.add_signer(
                            signature_request["id"],
                            document["id"],
                            demandes.client.first_name,
                            demandes.client.last_name,
                            demandes.client.email
                        )

                        # 6. Activate signature request
                        client.activate(
                            signature_request["id"]
                        )

                        # Save Yousign information
                        demandes.save(
                            update_fields=[
                                "yousign_request_id",
                                "yousign_document_id",
                            ]
                        )

                        messages.success(
                            request,
                            "La demande de location a été acceptée "
                            "et le contrat a été envoyé pour signature."
                        )

                    elif new_status == "accepté" and old_status == "accepté":

                        # Already accepted.
                        # Don't create another Yousign request.
                        messages.success(
                            request,
                            "La demande de location a été mise à jour."
                        )

                    else:

                        messages.success(
                            request,
                            "Vous venez de répondre à une demande cliente."
                        )
                        
                    # if the status new equal to rejeté do something:
            except Exception:
                logger.exception("Yousign failed")
            
                messages.error(
                    request,
                    "Erreur lors de la création du contrat Yousign"
                )
                            
            return redirect("locations:redirect_after_responding")  
             
        #If form is invalid, the page will be rendered again

    else:
        form = Reply_locatioForm(
            instance=demandes
        )

    context = {
        "demandes": demandes,
        "form": form,
        "dossier": dossier,
        "count": count,
        "booking_pending": booking_pending,
        "count_booking_pending": count_booking_pending,
    }

    return render(
        request,
        "administration/repondre_location.html",
        context
    )

#redirect the admin after responding to a location demande:
def redirect_after_responding(request):
    
    # all achat demande pending for the admin:
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #getting all pending demande  location for the admin and count them:
    dossier_location=DossierLocation.objects.filter(status ="encours")
    count_location=dossier_location.count()
    
    #count all demande booking in the system:
    all_demandes=DossierLocation.objects.all().order_by('-id')
    count_all_demandes=all_demandes.count()
    
    #all  demande en location in the system:ou en location running:
    all_sold=DossierLocation.objects.filter(status="en location")
    count_all_sold=all_sold.count()
    
    #get all booking car:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    context={
        'dossier':dossier,
        'count':count,
        'dossier_location':dossier_location,
        'count_location':count_location,
        'count_all_demandes':count_all_demandes,
        "all_demandes":all_demandes,
        'count_all_sold':count_all_sold,
    }
    return render(request,"administration/result.html",context)


# payement checkout de stripe de location:
def location_car(request, id):

    location_dossier = get_object_or_404(
        DossierLocation,
        id=id,
        client=request.user
    )
    
    # here i calculate the days of booking like:3 days of booking:
    days = (
    location_dossier.date_retour - location_dossier.date_depart
    ).days
     
    # if the date is less than zero: 
    if days <= 0:
      return HttpResponse(
        "Invalid rental dates.",
        status=400
    )
    
    # get the total days of booking:
    total_price = location_dossier.vehicule.prix * days
      
    # Check if the car is already rented
    if location_dossier.deal == "en location":
        return HttpResponse(
            "This car has already been booked."
        )

    # Stripe expects cents
    amount_cents = int(
        Decimal(str(total_price)) * 100
    )

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        mode="payment",

        line_items=[
            {
                "price_data": {
                    "currency": "eur",

                    "unit_amount": amount_cents,

                    "product_data": {
                        "name": (
                            f"{location_dossier.vehicule.marque} "
                            f"{location_dossier.vehicule.modele}"
                        ),
                    },
                },

                "quantity": 1,
            }
        ],

        customer_email=request.user.email,

        customer_creation="always",

        metadata={
            "type": "location",
            "location_id": str(location_dossier.id),
            "car_id": str(location_dossier.vehicule.id),
            "user_id": str(request.user.id),
            "days": str(days),
            "date_debut": str(location_dossier.date_depart),
            "date_fin": str(location_dossier.date_retour),
        },

        success_url=request.build_absolute_uri(
            "/payment-success/"
        ),

        cancel_url=request.build_absolute_uri(
            "/payment-cancel/"
        ),
    )

    # Save Stripe session ID
    location_payment = payementLocation.objects.create(
    location=location_dossier,
    stripe_session_id=session.id,
)

    return redirect(session.url)


# here the user check the raison why the demand is rejected or accepted in Achat mode:
def check_raison_booking(request, id):
       
    notification=DossierAchat.objects.filter(client=request.user,verification__in=['accepté','rejeté'],mysignature='not yet')
    count_notification=notification.count()
    
    #getting the demandes location:
    demande=get_object_or_404(DossierLocation,id=id,status__in=['rejeté','accepté'],mysignature='signé')
    
    context={
        'demande':demande,
        'notification':notification,
        'count_notification': count_notification
    }
    return render(request,'check_raison_booking.html',context) 


#the user search location demande by it unique code::
def user_search_location(request):
    query = request.GET.get("q", "").strip()

    if query == "":
        contract = DossierLocation.objects.filter(
            client=request.user
        ).order_by("-id")

    elif len(query) >= 2:
        contract = DossierLocation.objects.filter(
            Q(code_location__icontains=query),
            client=request.user
        ).order_by("-id")

    else:
        contract = DossierLocation.objects.none()

    for demande in contract:
        days = (demande.date_retour - demande.date_depart).days
        price = demande.vehicule.prix

        demande.days = days
        demande.total = price * days

    context = {
        "query": query,
        "contract": contract,
        "total": contract.count(),
    }

    # AJAX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "user_search_location_ajax.html",
            context
        )

    return render(
        request,
        "user_search_location_ajax.html",
        context
    )


#the user search achat demande by it unique code::
def user_search_achat(request):
    query = request.GET.get("q", "").strip()

    if query == "":
        contract = DossierAchat.objects.filter(
            client=request.user
        ).order_by("-id")

    elif len(query) >= 2:
        contract = DossierAchat.objects.filter(
            Q(code_dossier__icontains=query),
            client=request.user
        ).order_by("-id")

    else:
        contract = DossierAchat.objects.none()


    context = {
        "query": query,
        "contract": contract,
        "total": contract.count(),
    }

    # AJAX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "user_search_achat_ajax.html",
            context
        )

    return render(
        request,
        "user_search_achat_ajax.html",
        context
    )
    
# get booking encours live:
def live_booking(request):
    # Get all ongoing bookings
    ongoing_bookings = DossierLocation.objects.filter(
        deal="en location"
    ).order_by("-id")

    for demande in ongoing_bookings:
        days = (demande.date_retour - demande.date_depart).days
        price = demande.vehicule.prix

        demande.days = days
        demande.total = price * days

    context = {
        "ongoing_bookings": ongoing_bookings,
        "total": ongoing_bookings.count(),
    }

    return render(
        request,
        "administration/live_booking.html",
        context
    )  
    
    
#the user search location demande by it unique code::
def admin_search_ongoing_bookings(request):
    query = request.GET.get("q", "").strip()

    if query == "":
        ongoing_bookings = DossierLocation.objects.filter(
               deal="en location"
           ).order_by("-id")

    elif len(query) >= 2:
        ongoing_bookings = DossierLocation.objects.filter(
            Q(code_location__icontains=query),
            deal="en location"
            ).order_by("-id")

    else:
        ongoing_bookings = DossierLocation.objects.none()

    for demande in ongoing_bookings:
        days = (demande.date_retour - demande.date_depart).days
        price = demande.vehicule.prix

        demande.days = days
        demande.total = price * days

    context = {
        "query": query,
        "ongoing_bookings": ongoing_bookings,
        "total": ongoing_bookings.count(),
    }

    # AJAX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "administration/ajax/live_ajax.html",
            context
        )

    return render(
        request,
        "administration/ajax/live_ajax.html",
        context
    )
      
