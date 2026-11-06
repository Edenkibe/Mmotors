from django.shortcuts import render,get_object_or_404,redirect
from apps.voiture.models import Voiture,Photo
from django.db.models import Prefetch
from apps.promotion.models import Promotion
from apps.location.models import DossierLocation
from apps.promotion.forms.promoForm import promotionForm, Promo_modificationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q

from apps.dossiers.models import DossierAchat

# Create your views here.
def create_promotion(request, id):
   #get the orphanage of the user connected to create the mission
    get_car=get_object_or_404(Voiture, id=id)   
    #get all car picture 
    photos=Photo.objects.filter(voiture=get_car)
    
    if request.method == 'POST':
        form = promotionForm(request.POST)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.voiture = get_car
            promotion.creator = request.user
            promotion.user=request.user
            promotion.disponibilite="disponible"
            promotion.save()
            messages.success(request, 'vous venez de creer une publicité pour cette voiture')
            return redirect('core:car_details', id=get_car.id)
    else:
        form =promotionForm()
    
    return render(request, 'create_pub.html', {'form': form,'get_car':get_car,'photos':photos })


#admin view to see all advertise
def view_all_ads(request):
    
     #ici je fecth la promotion de toute les voitures  ainsi que leur photo main limite 1 et shuffle:
    promo = (
        Promotion.objects
        .filter(
            voiture__disponibilite="visible",
        )
        .select_related("voiture")
        .prefetch_related(
            Prefetch(
                "voiture__photos",
                queryset=Photo.objects.filter(is_main=True),
            )
        )
    )
    count_promo=promo.count()
    
    #count ads running now:
    count_promo_running=Promotion.objects.filter(disponibilite="commencé").count()
    done_promo=Promotion.objects.filter(disponibilite="promotion done").count()
    bloque_promo=Promotion.objects.filter(disponibilite="Bloqué").count()
    
    #getting all pending demande d achat et location for the admin and count them:   
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all booking car:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
        
        
    context={
        'promo':promo,
        'count_promo':count_promo,
        'dossier':dossier,
        'count':count,
        'count_promo_running':count_promo_running,
        'done_promo':done_promo,
        'bloque_promo':bloque_promo,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending
    }
    return render(request,'administration/ads.html',context)

#here the admin bloque une publicité et la debloque:
def bloque_unbloque(request,id):
    
    promo=get_object_or_404(Promotion,id=id)
    if promo.disponibilite in ['disponible','commencé','promotion done']:
        #on change le type achat en location
      promo.disponibilite="Bloqué"
    else:   
        promo.disponibilite="disponible"
    promo.save()
    
    return JsonResponse({
        "result":"success",
        "type": promo.disponibilite,
        "button_text": "La promo est disponible" if promo.disponibilite == "disponible" else "cette pub est suspendue"
    
    })
  
#modifier la pub:
def modifier_pub(request,id):
    
    #am getting a promotion with his car and one main photo of the car
    promo = get_object_or_404(
    Promotion.objects
    .filter(voiture__disponibilite="visible")
    .select_related("voiture")
    .prefetch_related(
        Prefetch(
            "voiture__photos",
            queryset=Photo.objects.filter(is_main=True),
        )
    ),
    id=id,
    ) 

    
    if request.method == 'POST':
        form = Promo_modificationForm(request.POST, instance=promo)  # inserer l instance car dans la form
        if form.is_valid():
            form.save()  # saves the edits
            messages.success(request,'promotion modifier avec succée')
            return redirect('core:car_details', id=id)
           
    else:
        form = Promo_modificationForm(instance=promo)  # populate form with existing data
    
    return render(request, 'modif_pub.html', {'form': form,'promo':promo })  


#delete ads    
def delete_ads(request,id):
     #get the member
    promo=get_object_or_404(Promotion,id=id) 
     
    marque=promo.voiture.marque #sauvegarder la voiture avant de la supprimer
    modele=promo.voiture.modele
    promo.delete()
         
    messages.success(request,f"La promotion pour La voiture  {marque},{modele} a été supprimer avec succées")        
    return redirect('promotion:view_all_ads') 

#the admin search promotion:
def admin_search_ads(request):
    query = request.GET.get("q", "").strip()

    #je recupere toutes le promotion liée a des voitures ainsi que leur photo principale
    base_queryset = (
        Promotion.objects
        .filter(voiture__disponibilite="visible")
        .select_related("voiture")
        .prefetch_related(
            Prefetch(
                "voiture__photos",
                queryset=Photo.objects.filter(is_main=True),
            )
        )
    )

    # If the search bar is empty, return all promotions
    if query == "":
        results = base_queryset

    #si la baree de recherche n est pas vide :on filtre
    elif len(query) >= 2:
        filters = (
            Q(disponibilite__icontains=query) |
            Q(titre__icontains=query)
        )

        results = base_queryset.filter(filters)

    else:
        results = Promotion.objects.none()

    context = {
        "query": query,
        "results": results,
        "total": results.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "partial_ajax/result_search_promo.html",
            context,
        )