from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import Prefetch,Exists,OuterRef
from apps.voiture.models import Voiture,Photo
from apps.location.models import DossierLocation
from apps.voiture.forms.voitureForm import VoitureForm, PhotoForm
from apps.dossiers.models import DossierAchat
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
import logging
from apps.voiture.service import invoice
logger = logging.getLogger(__name__)
from datetime import date, datetime
#to save the contract signed in the db:
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def show_voitures(request):
    return render(request, 'voiture/voitures.html')

# fetch all car pour la vente
def vente_car(request):
    
    #get all the cars from the database: with one main picture for each car for achat:
    cars = Voiture.objects.filter(disponibilite="Visible",type="Achat").annotate(
        #compter le nombre de fois que cette voiture est demandée pour l achat
        dossier_count=Count("dossiers_voitures"), # name related name of car in achat modele
        has_achat=Exists(
                DossierAchat.objects.filter(
                    vehicule=OuterRef("pk"),
                    verification="pending...",
                    client=request.user
                )
        )
    ).prefetch_related(
     Prefetch(
        "photos", #photos is the related name of voiture in photo model
        queryset=Photo.objects.filter(is_main=True)#getting the main picture
    )
)
    
    #ici je veux fetch que le marques de voitures inscrite et esquiver les doublons:
    #Obtenir chaque marque avec le nombre de voitures
    #marques = Voiture.objects.values('marque').distinct() eviter le doublon only
    marques = (
    Voiture.objects.filter(type="Achat")
    .values("marque")
    .annotate(nombre_voitures=Count("id"))
    .order_by("marque")
)
    return render(request,"car_vente.html",{"cars":cars,"marques":marques})


#search car only in type achat:
def search_car_achat(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne toute les voiture
    if query == "":
        
         results = Voiture.objects.filter(disponibilite="Visible",type="Achat").annotate(
                #compter le nombre de fois que cette voiture est demandée pour l achat
                dossier_count=Count("dossiers_voitures"), # name related name of car in achat modele
                has_achat=Exists(
                        DossierAchat.objects.filter(
                            vehicule=OuterRef("pk"),
                            verification="pending...",
                            client=request.user
                        )
                )
            ).prefetch_related(
             Prefetch(
                "photos", #photos is the related name of voiture in photo model
                queryset=Photo.objects.filter(is_main=True)#getting the main picture
            )
        )

    elif len(query) >= 2:
        filters = (
            Q(marque__icontains=query) |
            Q(modele__icontains=query) |
            Q(prix__icontains=query) 
        )

        results = Voiture.objects.filter(filters,disponibilite="Visible",type="Achat").annotate(
                #compter le nombre de fois que cette voiture est demandée pour l achat
                dossier_count=Count("dossiers_voitures"), # name related name of car in achat modele
                has_achat=Exists(
                        DossierAchat.objects.filter(
                            vehicule=OuterRef("pk"),
                            verification="pending...",
                            client=request.user
                        )
                )
                ).prefetch_related(
                 Prefetch(
                    "photos", #photos is the related name of voiture in photo model
                    queryset=Photo.objects.filter(is_main=True)#getting the main picture
            )
        )

    else:
        results = Voiture.objects.none()

    context = {
        "query": query,
        "results": results,
        "total": results.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "admin_template/partials/get_car_ajax_result.html",
            context,
        )

    return render(request, "admin_template/search_car_vente.html", context)



# fetch all car pour la location
def location_car(request):   
    #getting the user connected:
    user_connected=request.user
    
    #get all the cars from the database: with one main picture for each car for achat:
    cars = Voiture.objects.filter(disponibilite="Visible",type="Location").annotate(
        # how many people are requesting this car dossiers_location_voitures is related name of car in location modele: 
        dossier_count=Count("dossiers_location_voitures"),
        # checking if the car is in the location:
            is_location=Exists(
                DossierLocation.objects.filter(
                    vehicule=OuterRef("pk"),
                    status__in=["accepté","signé"],
                    deal="en location"                
                )
            )
    ).prefetch_related(
     Prefetch(
        "photos", #photos is the related name of voiture in photo model
        queryset=Photo.objects.filter(is_main=True)#getting the main picture
    )
)
    
    #ici je veux fetch que le marques de voitures inscrite et esquiver les doublons:
    #Obtenir chaque marque avec le nombre de voitures
    #marques = Voiture.objects.values('marque').distinct() eviter le doublon only
    marques = (
    Voiture.objects.filter(type="Location")
    .values("marque")
    .annotate(nombre_voitures=Count("id"))
    .order_by("marque")
)
    
    context={
       "cars":cars,
       "marques":marques,
       "user_connected":user_connected
    }
    return render(request,"location.html",context)

#search the location car by the date:
def recherche_voitures(request):

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    #here we calculate the date in days to multiply it with the price of the cars:
    # here i calculate the days of booking like:3 days of booking: we need to convert them to dates: 
    begin_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    finish_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    days = (finish_date - begin_date).days
    

    # la datte de retour doit être après la date de début, sinon on retourne une erreur: pour 1 jour 
    if days <= 0:
        return render(request, "faile_request.html", status=400)
    
    cars = Voiture.objects.none()
    erreur = None
    count_cars=0

    if start_date and end_date:

        # Conversion des dates
        start_date_obj = date.fromisoformat(start_date)
        end_date_obj = date.fromisoformat(end_date)
        
        # conversion date en frncais ex: 12 aout 2026:
        mois = {
            1: "janvier",
            2: "février",
            3: "mars",
            4: "avril",
            5: "mai",
            6: "juin",
            7: "juillet",
            8: "août",
            9: "septembre",
            10: "octobre",
            11: "novembre",
            12: "décembre",
        }
        start_date_formatted = (
         f"{start_date_obj.day} {mois[start_date_obj.month]} {start_date_obj.year}"
        )

        end_date_formatted = (
        f"{end_date_obj.day} {mois[end_date_obj.month]} {end_date_obj.year}"
        )

        # Vérification des dates
        if start_date_obj >= end_date_obj:

            erreur = "La date de retour doit être après la date de début."

        else:

            # Recherche des voitures disponibles
            # on compare le date inversement donc date depart=date retour etc..
            cars = Voiture.objects.filter(type="Location").exclude(
                dossiers_location_voitures__date_depart__lt= end_date_obj,
                dossiers_location_voitures__date_retour__gt=start_date_obj,
                dossiers_location_voitures__deal__in=['en location','commencé'],
            ).distinct()
            
            count_cars=cars.count()

    context = {
        "cars":cars,
        'start_date_formatted':start_date_formatted,
        'end_date_formatted':end_date_formatted,
        'erreur':erreur,
        'count_cars':count_cars,
        'days':days,
    }

    return render(
        request,
        "admin_template/search_car_location.html",
        context
    )
    
#search car only in type location:
def search_car_location(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne toute les voiture
    if query == "":
        results = Voiture.objects.filter(disponibilite="Visible",type="Location").prefetch_related(
            Prefetch(
                "photos",
                queryset=Photo.objects.filter(is_main=True)
            )
        )

    elif len(query) >= 2:
        filters = (
            Q(marque__icontains=query) |
            Q(modele__icontains=query)
        )

        results = Voiture.objects.filter(filters,disponibilite="visible",type="Location").prefetch_related(
            Prefetch(
                "photos",
                queryset=Photo.objects.filter(is_main=True)
            )
        )

    else:
        results = Voiture.objects.none()

    context = {
        "query": query,
        "results": results,
        "total": results.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "admin_template/partials/get_car_ajax_result.html",
            context,
        )

    return render(request, "admin_template/search_car.html", context)
#________________________________________________________________________________
#integration stripe:

# checkout session to buy a car:
def buy_car(request, id): 
    # we did this because multiple users can try to buy the same car: we did vehicule__id=id que: vehicule=id  
    achat_dossier = get_object_or_404(DossierAchat, id=id,client=request.user)
    amount = float(achat_dossier.vehicule.prix) 
  # Stripe attend le montant en centimes
    amount_cents = int(achat_dossier.vehicule.prix * 100)
   
    if achat_dossier.deal == "acheté":
        return HttpResponse("This car has already been sold.")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",

        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": amount_cents,
                    "product_data": {
                        "name": f"{achat_dossier.vehicule.marque} {achat_dossier.vehicule.modele}",
                    },
                },
                "quantity": 1,
            }
        ],
        customer_email=request.user.email, 
        customer_creation="always",
       
        metadata={
            "type": "achat",
            "achat_id": str(achat_dossier.id),
            "car_id": achat_dossier.vehicule.id,
            "user_id": request.user.id,
            "description": f"acheteur  {achat_dossier.nom_complet}",
        },

        success_url=request.build_absolute_uri("/payment-success/"),
        cancel_url=request.build_absolute_uri("/payment-cancel/"),
    )
    
    # am Saving Stripe session ID in the db:
    achat_dossier.stripe_session_id = session.id
    achat_dossier.save()
    
    return redirect(session.url)

# success page:
def success(request):
    return render(request,"success_payement.html")

# cancel page:
def cancel(request):
    return render(request,"payement_cancel.html")

#admin delete all cars:
def delete_all_cars(request):
    Voiture.objects.all().delete() 
    messages.success(request, "All cars have been deleted successfully.")
    return redirect("core:admin_page")

# add voiture or car for the admin:
def add_voiture(request):
    # get all new achat demande with pending...
    demande_pending = DossierAchat.objects.filter(verification="pending...")
    count_pending_demandes=demande_pending.count()
    
    #get all new booking car demande:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    if request.method == "POST":
        form = VoitureForm(request.POST)

        if form.is_valid():
            voiture = form.save(commit=False)
            voiture.date_added = timezone.now()
            voiture.save()
            messages.success(request, f'vous venez d\'ajouter {voiture.marque} {voiture.modele} a la liste des voitures')
            return redirect("voitures:add_voiture")
        else:
            print(form.errors)      # <-- Check this
            print(form.cleaned_data if form.is_bound else "")
    else:
        form = VoitureForm()

    context={
        "form": form,
        'demande_pending':demande_pending,
        'count_pending_demandes':count_pending_demandes,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending,
    }
    return render(request, "administration/add_voiture.html",context)


# add a photo for a voiture or car for the admin:
def add_voiture_photo(request,id):
    voiture=get_object_or_404(Voiture, id=id)
    
    # get all new achat demande with pending...
    demande_pending = DossierAchat.objects.filter(verification="pending...")
    count_pending_demandes=demande_pending.count()
        
    #get all new booking car demande:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.voiture = voiture
            photo.date_added = timezone.now()
            photo.save()
            messages.success(request, f'vous venez d\'ajouter une photo pour {photo.voiture.marque} {photo.voiture.modele}')
            return redirect("voitures:add_voiture_photo", id=voiture.id)
        else:
            print(form.errors)      # <-- Check this
            print(form.cleaned_data if form.is_bound else "")
    else:
        form = PhotoForm()
    
    context={
            "form": form,
            'demande_pending':demande_pending,
            'count_pending_demandes':count_pending_demandes,
            'booking_pending':booking_pending,
            'count_booking_pending':count_booking_pending,
            "voiture": voiture
        }
    return render(request, "administration/add_photo_voiture.html",context)
    
