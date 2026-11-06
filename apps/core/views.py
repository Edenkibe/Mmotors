from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import OuterRef, Prefetch,Exists
from apps.voiture.models import Voiture,Photo
from apps.promotion.models import Promotion
from apps.accounts.models import User
from apps.voiture.forms.voitureForm import VoitureForm,typeForm
from apps.dossiers.models import DossierAchat
from apps.location.models import DossierLocation,payementLocation
from apps.dossiers.form.reply_demandeForm import ReplydossierForm
from django.db.models import Count
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Sum
from apps.core.yousignservice import YousignClient
import logging
logger = logging.getLogger(__name__)
from django.db import transaction
#to save the contract signed in the db:
from django.views.decorators.csrf import csrf_exempt


# home page, ici on cherche la voiture en location:
def home_page(request):
    
    #ici je fecth la promotion de toute les voitures  ainsi que leur photo main limite 1 et shuffle:
    promo = (
        Promotion.objects
        .filter(
            disponibilite="commencé",
            voiture__disponibilite="visible",
        )
        .select_related("voiture")
        .prefetch_related(
            Prefetch(
                "voiture__photos",
                queryset=Photo.objects.filter(is_main=True),
            )
        )
        .order_by("?")
        .first()
    )
    
    if request.user.is_authenticated:
       #notification for user check if the user dossier to buy a car has been accepted: he has to sign the contract
       notification=DossierAchat.objects.filter(client=request.user,verification__in=['accepté','rejeté'],mysignature='not yet')
       count_notification=notification.count()
       
       #getting all location or booking notification for the user:
       notification_location=DossierLocation.objects.filter(client=request.user,status__in=['accepté','rejeté'],mysignature='not yet')
       count_notification_location=notification_location.count()
       
       
       #admin notification getting all pending demande d achat  for the admin and count them:   
       dossier=DossierAchat.objects.filter(verification ="pending...")
       count=dossier.count()
       
       #admin notification getting all pending demande of bookings  for the admin and count them:   
       dossier_location=DossierLocation.objects.filter(status ="encours")
       count_location=dossier_location.count()
    else:
       # if is not log in we shall not show the count notification: 
       notification = DossierAchat.objects.none()
       count_notification = 0  
       
       dossier = DossierAchat.objects.none()
       count = 0
       
       notification_location=DossierLocation.objects.none()
       count_notification_location= 0
       
       dossier_location=DossierLocation.objects.none()
       count_location= 0
       
    context={
        'promo':promo,
        'notification':notification,
        'count_notification':count_notification,
        'dossier':dossier,
        'count':count,
        'dossier_location':dossier_location,
        'count_location':count_location,
        'notification_location':notification_location,
        'count_notification_location':count_notification_location
    }
    return render(request,"homepage/index.html",context)

        
#timeline page
def timeline_page(request):
    return render(request,"timeline/timeline.html")

#admin template
def admin_page(request):
    
    #getting all pending demande d achat for the admin and count them:   
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #count all cars in the system:
    all_cars=Voiture.objects.filter(disponibilite="visible")
    count_all_cars=all_cars.count()
    
    # on va compter le nombre de voitures qui sont vendus en action maintenant pour permettre a l admin de le suivre 
    # pour contacter le client :
    action=DossierAchat.objects.filter(deal="acheté",read="non lu").count()
    
    #pourcentage de voiture vendu par rapport au nombre total de voiture:
    sold_cars=Voiture.objects.filter(disponibilite="acheté").count()
    all_cars_count=Voiture.objects.all().count()
    percentage_sold = (
        sold_cars / all_cars_count * 100
        if all_cars_count > 0
        else 0
    )
    percentage_voiture_restante=(
        count_all_cars / all_cars_count * 100
        if all_cars_count > 0
        else 0
    )
    
    # here to calculate the amount total sold cars in achat mode:
    total_sold_car = DossierAchat.objects.filter(
        deal="acheté"
    ).aggregate(
        total=Sum("paid_amount")
    )["total"] or 0
    
    # calcule global somme de payement location:
    total_booking_somme=payementLocation.objects.aggregate(
            total=Sum("paid_amount")
        )['total'] or 0
    
    
    location_cars=Voiture.objects.filter(type="Location").count()    
    achat_cars=Voiture.objects.filter(type="Achat",disponibilite="visible").count()
   
    vendu_cars=Voiture.objects.filter(type="Achat",disponibilite="acheté")
    count_vendu_cars=vendu_cars.count()
    
    # get all demande done :
    dossier_user = DossierAchat.objects.all()
    count_all_demandes=dossier_user.count()
    
    # get all new achat demande with pending...
    demande_pending = DossierAchat.objects.filter(verification="pending...")
    count_pending_demandes=demande_pending.count()
    
    acheved_demandes = DossierAchat.objects.filter(verification="accepté")
    count_acheved_demandes=acheved_demandes.count()
    
    rejeted_demandes = DossierAchat.objects.filter(verification="rejeté")
    count_rejeted_demandes=rejeted_demandes.count()
    
    # get all user in the system:
    all_users=User.objects.filter().all()   
    count_all_users=all_users.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # on calclcule le pourcentage d'utilisateurs actifs par rapport au nombre total d'utilisateurs:     
    percentage_active = (
    active_users / count_all_users * 100
    if count_all_users > 0
    else 0
)
    
    #get all new  booking car demande:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
        
    acheved_booking = DossierLocation.objects.filter(status="accepté")
    count_acheved_bookings=acheved_booking.count()
        
    runnung_booking = DossierLocation.objects.filter(deal="en location")
    count_running=runnung_booking.count()
    
    rejeté_booking = DossierLocation.objects.filter(status="rejeté")
    count_rejeté=rejeté_booking.count()
    
    # getting all ads running in the system:
      #ici je fecth la promotion de toute les voitures  ainsi que leur photo main limite 1 et shuffle:
    promo = (
            Promotion.objects
            .filter(
                disponibilite="commencé",
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
      
    context={
        'dossier':dossier,
        'count':count,
        'count_all_cars':count_all_cars,
        'location_cars':location_cars,
        'achat_cars':achat_cars,
        'count_vendu_cars':count_vendu_cars,
        'count_all_demandes':count_all_demandes,
        'count_pending_demandes':count_pending_demandes,
        'count_acheved_demandes':count_acheved_demandes,
        'count_rejeted_demandes':count_rejeted_demandes,
        'count_all_users':count_all_users,
        'count_promo':count_promo,
        "promo":promo,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending,
        'count_acheved_bookings':count_acheved_bookings,
        'count_running':count_running,
        'count_rejeté' :count_rejeté,
        "percentage_active":percentage_active,
        "percentage_sold":percentage_sold,
        'percentage_voiture_restante':percentage_voiture_restante,
        'total_sold_car':total_sold_car,
        "total_booking_somme":total_booking_somme,
        'action':action
        }
    return render(request,"administration/index.html",context)


# action admin to see the car sold now now to contact the client:
def action_admin(request):
    # get all cars sold now:
    action=DossierAchat.objects.filter(deal="acheté",read__in=["non lu","lu"])
    count_action=action.count()
    
    context={
        'action':action,
        'count_action':count_action
    }
    return render(request,'administration/action.html',context)


# search action car sold now now to contact the client:with ajax:
def search_action(request):
    query=request.GET.get("q","").strip()
    
    #si la barre est vide on retourne tout le user
    if query == "":
        action = DossierAchat.objects.filter(deal="acheté",read__in=["non lu","lu"])

    elif len(query) >= 2:
        filters = (
            Q(code_dossier__icontains=query) |
            Q(client__first_name__icontains=query)|
            Q(client__last_name__icontains=query) 
        )

        action = DossierAchat.objects.filter(filters,deal="acheté",read__in=["non lu","lu"])

    else:
        action = DossierAchat.objects.none()

    context = {
        "query": query,
        "action": action,
        "total": action.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "ajax/action_ajax.html",
            context,
        )
        
    render(request, "ajax/action_ajax.html", context) 
    

#contact the client now after the car has been sold to him:
def contact_client(request,id):
    #get the car sold to the client:
    dossier=get_object_or_404(DossierAchat,id=id)
    
    # quand on click sur cette page on va marquer le dossier comme lu pour que l admin sache qu il a deja contacté le client:
    dossier.read="lu"
    dossier.save()
    
    context={
        'dossier':dossier
    }
    return render(request,'administration/contact_client.html',context)  

   
#show cars pour l administrateur
def show_cars_admin(request):
    
    #get all the cars from the database: with one main picture for each car:
    cars = Voiture.objects.filter(disponibilite="visible").annotate(
        dossier_count=Count("dossiers_voitures"),
        # check if the car has a promotion running,disponible or  not:
        has_promotion=Exists(
        Promotion.objects.filter(
            voiture=OuterRef("pk"),
            disponibilite__in=["commencé", "disponible"]
        )
        )
    ).prefetch_related(
     Prefetch(
        "photos", #photos is the related name of voiture in photo model
        queryset=Photo.objects.filter(is_main=True)#getting the main picture
    )
    )
    #count cars:
    count_cars=cars.count()
    
    #getting all pending demande d achat et location for the admin and count them:   
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all booking car:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    #ici je veux fetch que le marques de voitures inscrite et esquiver les doublons:
    #Obtenir chaque marque avec le nombre de voitures
    #marques = Voiture.objects.values('marque').distinct() eviter le doublon only
    marques = (
    Voiture.objects
    .values("marque")
    .annotate(nombre_voitures=Count("id"))
    .order_by("marque")
)
      
    context={
        "cars":cars,
        "marques":marques,
        "dossier":dossier,
        "count":count,
        "count_cars":count_cars,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending
        }
    return render(request,"administration/manage_car.html",context)

#admin seeing cars by id
def car_details(request,id):
    
    #get the car by its id with one picture main each
    get_car = get_object_or_404(
        Voiture.objects.prefetch_related(
            Prefetch(
                "photos",
                queryset=Photo.objects.filter(is_main=True)
            )
        ),
        id=id
    )
    
    #get all car picture 
    photos=Photo.objects.filter(voiture=get_car)
    
    # if this voiture existe deja dans la table promotion est que la 
    # disponibilite == to disponible on ne cree plus un pub pour cette voiture
    
    check=Promotion.objects.filter(voiture=get_car).exists()
    
    context={
        'get_car':get_car,
        'photos':photos,
        'check':check
    }
    return render(request,'admin_template/car_details.html',context)
                  

#this is for the user searching car:
def admin_search_voiture(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne toute les voiture
    if query == "":
        results = Voiture.objects.filter(disponibilite="Visible").prefetch_related(
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

        results = Voiture.objects.filter(filters,disponibilite="visible").prefetch_related(
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


#this is for the admin searching car in the dashboard:
def admin_search_car(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne toute les voiture
    if query == "":
        results = Voiture.objects.filter(disponibilite="visible").annotate(
            # check if the car has a promotion running,disponibel or  not:
            has_promotion=Exists(
            Promotion.objects.filter(
                voiture=OuterRef("pk"),
                disponibilite__in=["commencé", "disponible"]
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
            Q(modele__icontains=query)
        )

        results = Voiture.objects.filter(filters,disponibilite="visible").annotate(
                # check if the car has a promotion running,disponibel or  not:
                has_promotion=Exists(
                Promotion.objects.filter(
                    voiture=OuterRef("pk"),
                    disponibilite__in=["commencé", "disponible"]
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
            "admin_template/partials/admin_get_car.html",
            context
        )
   
#admin changing the etat of voiture achat en location vice versa:
def basculer_type(request,id):
    #get the car by its id with one picture main each
    get_car = get_object_or_404(
        Voiture.objects.prefetch_related(
            Prefetch(
                "photos",
                queryset=Photo.objects.filter(is_main=True)
                )
            ),
            id=id
        )
        
     #get all car picture 
    photos=Photo.objects.filter(voiture=get_car)
    
    if request.method == 'POST':
            form = typeForm(request.POST, instance=get_car)  # inserer l instance car dans la form
            if form.is_valid():
                form.save()  # saves the edits
                messages.success(request,'car has been edited successfully')
                return redirect('core:basculer_type', id=id)
               
    else:
        form = typeForm(instance=get_car)  # populate form with existing data
    
    context={
            'get_car':get_car,
            'photos':photos, 
            "form":form        
        }
    return render(request,'admin_template/bascule_type.html',context)
    

#admin changing the disponibilite of voiture  visible to invisible:
def change_disponibilite(request,id):
    cars=get_object_or_404(Voiture,id=id)
    if cars.disponibilite == "visible":
        #on change le type achat en location
      cars.disponibilite="invisible"
    else:   
        cars.disponibilite="visible"
    cars.save()
    
    return JsonResponse({
        "result":"success",
        "type": cars.disponibilite,
        "button_text": "La voiture est visible" if cars.disponibilite == "visible" else "La voiture est invisible"
    }) 
    
#admin deletes a car:
def delete_car(request,id):
    #get the member
     cars=get_object_or_404(Voiture,id=id) 
     
     marque=cars.marque #sauvegarder la voiture avant de la supprimer
     modele=cars.modele
     cars.delete()
         
     messages.success(request,f"La voiture  {marque},{modele} a été supprimer avec succées")        
     return redirect('core:show_cars_admin')
           
    
#editing the car info
def edit_car(request, id):
    get_car = get_object_or_404(Voiture, id=id)  # fetch the car

    if request.method == 'POST':
        form = VoitureForm(request.POST, instance=get_car)  # inserer l instance car dans la form
        if form.is_valid():
            form.save()  # saves the edits
            messages.success(request,'car has been edited successfully')
            return redirect('core:car_details', id=id)
           
    else:
        form = VoitureForm(instance=get_car)  # populate form with existing data
    
    return render(request, 'admin_template/modifier_car.html', {'form': form,'get_car':get_car })

#________________________________________________________________________________________________

#the admin manage user 

def admin_manage_user(request):
    
    #get all users
    users=User.objects.filter().all()
    
    #getting all pending demande d achat et location for the admin and count them:   
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all booking car:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    count_user=users.count()
    context={
        'users':users,
        'count_user':count_user,
        'dossier': dossier,
        'count':count,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending
    }
    
    return render(request,'administration/user.html',context)

#block and unblock user
#admin changing the disponibilite of voiture  visible to invisible:
def block_unblock_user(request,id):
    user=get_object_or_404(User,id=id)
    # ==========================
    # User Management Functions

    #if users.is_active is True:
        #on change le type achat en location
    #   users.is_active = False
    #else:   
    #     users.is_active = True
    # ==========================
    
    #or simply i can do:
    user.is_active = not user.is_active     
    user.save()
    
    return JsonResponse({
        "result":"success",
        "type": user.is_active,
        "button_text": "Block this user ?" if user.is_active == True else "activate this user"
    }) 
    
#admin deletes a car:
def delete_user(request,id):
    #get the member
     user=get_object_or_404(User,id=id) 
     
     username=user.username #sauvegarder le nom avant de la supprimer
     email=user.email
     user.delete()
         
     messages.success(request,f"User {username},{email} a été supprimer avec succées")        
     return redirect('core:admin_manage_user')    
 
def view_user(request,id):
    #get the member
    user=get_object_or_404(User,id=id)
    
    context={
        'user':user
    } 
    return render(request,'admin_template/user_template/view_user.html',context)       
      

#the admin search user:
def admin_search_user(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne tout le user
    if query == "":
        users = User.objects.filter().all()

    elif len(query) >= 2:
        filters = (
            Q(username__icontains=query) |
            Q(first_name__icontains=query)
        )

        users = User.objects.filter(filters).all()

    else:
        users = User.objects.none()

    context = {
        "query": query,
        "users": users,
        "total": users.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "admin_template/partials/get_user_ajax.html",
            context,
        )
        
#------------------------------------------------------------------------------
#admin demande achat and location management!               

#repondre a une demande achat
def repondre(request,id):
    
    #getting all pending demande d achat et location for the admin and count them:
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all booking car en pendind de validation:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
        
    #admin is getting  a demande to reply to it:
    demandes=get_object_or_404(DossierAchat,id=id)
    
    #get the email of the demander:
    email_user=demandes.email
    if request.method == "POST":

        # Keep the old status BEFORE saving parce que si le status == accepte we proceed
        old_status = demandes.verification

        form = ReplydossierForm(request.POST, instance=demandes)

        if form.is_valid():

            try:
                with transaction.atomic():
                    # Save the form
                    demandes = form.save()

                    # New status after form submission
                    new_status = demandes.verification

                    # Only do Yousign when status becomes "accepté"
                    if new_status == "accepté" and old_status != "accepté":

                        client = YousignClient()

                        # 1. Generate PDF contract
                        client.generate_contract(
                            demandes,
                            "achat"
                        )
                        logger.info("STEP 1 SUCCESS: Contract PDF generated")

                        signature_request = client.create_signature_request(
                            demandes,
                            "achat"
                        )

                        logger.info("STEP 2 SUCCESS: Signature request: %s", signature_request)

                        document = client.upload_document(
                            signature_request["id"],
                            demandes.contrat_pdf.path
                        )

                        logger.info("STEP 3 SUCCESS: Document uploaded: %s", document)

                        signer = client.add_signer(
                            signature_request["id"],
                            document["id"],
                            demandes.client.first_name,
                            demandes.client.last_name,
                            demandes.client.email
                        )

                        logger.info("STEP 4 SUCCESS: Signer added: %s", signer)

                        activation = client.activate(signature_request["id"])

                        logger.info("STEP 5 SUCCESS: Request activated: %s", activation)

                        # 2. Create Yousign signature request
                        signature_request = client.create_signature_request(
                            demandes,
                            "achat"
                        )

                        demandes.yousign_request_id = signature_request["id"]

                        # 3. Upload PDF to Yousign
                        document = client.upload_document(
                            signature_request["id"],
                            demandes.contrat_pdf.path
                        )

                        demandes.yousign_document_id = document["id"]

                        # 4. Add client as signer
                        logger.info(client.add_signer(
                            signature_request["id"],
                            document["id"],
                            demandes.client.first_name,
                            demandes.client.last_name,
                            demandes.client.email
                        ))

                        # 5. Activate signature request
                        logger.info(client.activate(
                            signature_request["id"]
                        ))

                        # Save Yousign IDs
                        demandes.save(
                            update_fields=[
                                "yousign_request_id",
                                "yousign_document_id"
                            ]
                        )

                        messages.success(
                            request,
                            "La demande a été acceptée et le contrat a été envoyé pour signature."
                        )

                    elif new_status == "accepté" and old_status == "accepté":

                        messages.success(
                            request,
                            "La demande a été mise à jour."
                        )
                    
                    else:

                        messages.success(
                            request,
                            "Vous venez de répondre à une demande client."
                        )

            except Exception:
                logger.exception("Yousign failed")

                messages.error(
                    request,
                    "Erreur lors de la création du contrat Yousign"
                )
                
            return redirect("locations:redirect_after_responding")   
         
        # If form is invalid, stay on the page
    else:
        form = ReplydossierForm(instance=demandes)

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
        "administration/repondre_demande.html",
        context
    )
          

