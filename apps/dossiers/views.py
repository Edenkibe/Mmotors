from django.shortcuts import redirect, render,get_object_or_404
from apps.voiture.models import Voiture
from apps.dossiers.models import DossierAchat
from apps.location.models import DossierLocation
from apps.dossiers.form.dossierForm import DossierAchatForm
from django.contrib import messages
from django.db.models import Q


# success page de votre depot de dossier:
def success_dossier_depot(request):
    return render(request,'success_dossier_depot.html')

# depot de dossier pour achat!
def depot_dossier(request,id):   
    #get the car for the demande:
    get_car=get_object_or_404(Voiture,id=id)
    
    
    #if this exist in the dossier we shall show a text to the user that he already demanding this car:
    dossier_exist=DossierAchat.objects.filter(vehicule=get_car,client=request.user,verification='pending...').exists()
    count=DossierAchat.objects.filter(vehicule=get_car).count()
    
    if request.method == 'POST':
        form = DossierAchatForm(request.POST, request.FILES)
        if form.is_valid():
            dossier = form.save(commit=False)
            dossier.client =request.user  # user
            dossier.vehicule =get_car  # vehicule
           
            dossier.save()
            return redirect('dossiers:success_dossier_depot')    
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DossierAchatForm()

    context={
        'get_car':get_car,
        'form':form,
        'dossier_exist':dossier_exist,
        'count':count
    }
        
    return render(request,'depot_dossier.html',context)

# tell user to check is email to sign the contract if his file has been accepted:
def dossier_accepted(request):
    
    if request.user.is_authenticated:
        
        # once we are here in this page
        # notification user and check if the user dossier has been accepted: or rejected he has to sign the contract
        notification=DossierAchat.objects.filter(client=request.user,verification__in=['accepté','rejeté'],mysignature='not yet')
        count_notification=notification.count()
        
        #notification for booking of user if his demande is being accepted or rejected user action:
        notification_location=DossierLocation.objects.filter(client=request.user,status__in=['accepté','rejeté'],mysignature='not yet')
        count_notification_location=notification_location.count()
        
        #admin notification getting all pending demande d achat et location for the admin and count them:   
        dossier=DossierAchat.objects.filter(verification ="pending...")
        count=dossier.count()
    else:
        # if is not log in we shall not show the count notification: 
        notification = DossierAchat.objects.none()
        count_notification = 0 
        dossier = DossierAchat.objects.none()
        count = 0
         
    context={
        'dossier':dossier,
        'count':count,
        'notification':notification,
        'count_notification':count_notification,
        'notification_location':notification_location,
        'count_notification_location':count_notification_location
    }
    return render(request,"call_to_sign.html",context)


def all_demandes(request):
    
    #admin notification getting all pending demande d achat et location for the admin and count them:   
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all new booking car demande:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
        
    #count all demande in the system:
    all_demandes=DossierAchat.objects.all().order_by('-id')
    count_all_demandes=all_demandes.count()
    
    context={
        'dossier':dossier,
        'count':count,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending,
        'count_all_demandes':count_all_demandes,
        "all_demandes":all_demandes
    }
    return render(request,"administration/all_demande.html",context)
    
#the admin search dossier of user by it unique code::
def search_dossier(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne tout le user
    if query == "":
        dossier_user = DossierAchat.objects.filter().all()

    elif len(query) >= 2:
        filters = (
            Q(code_dossier__icontains=query)
        )

        dossier_user = DossierAchat.objects.filter(filters).all()

    else:
        dossier_user = DossierAchat.objects.none()

    context = {
        "query": query,
        "dossier_user": dossier_user,
        "total": dossier_user.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "admin_template/partials/all_demande_ajax.html",
            context,
        )
     # Retour pour les requêtes classiques
    return render(
        request,
        "admin_template/partials/all_demande_ajax.html",
        context,
    )    
 
 
def all_sold_demand(request):
    
    #admin notification getting all pending demande d achat et location for the admin and count them:   
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all booking car en pendind de validation:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    #count all sold demande in the system:
    all_sold=DossierAchat.objects.filter(deal="acheté")
    count_all_sold=all_sold.count() 
    
    context={
        'dossier':dossier,
        'count':count,
        "booking_pending": booking_pending,
        "count_booking_pending": count_booking_pending,
        "all_sold":all_sold,
        "count_all_sold" :count_all_sold
    }
    return render(request,"administration/sold_demand.html",context)        


#the admin search sold car  dossier of user by it unique code or modele and marque::
def search_sold_car(request):
    query = request.GET.get("q", "").strip()
    
    #si la barre est vide on retourne tout le dossier car vendu
    if query == "":
        sold_car = DossierAchat.objects.filter(deal="acheté")

    elif len(query) >= 2:
        filters = (
            Q(code_dossier__icontains=query)|
            Q(vehicule__marque__icontains=query)|
            Q(vehicule__modele__icontains=query)
        )

        sold_car = DossierAchat.objects.filter(filters)

    else:
        sold_car = DossierAchat.objects.none()

    context = {
        "query": query,
        "sold_car": sold_car,
        "total": sold_car.count(),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "admin_template/partials/sold_car_ajax.html",
            context,
        )
     # Retour pour les requêtes classiques
    return render(
        request,
        "admin_template/partials/sold_car_ajax.html",
        context,
    )    
        
# get the notification of the achat demande which is rejected by the admin: user action:
def rejected_notification(request, id):
    
    
    #fetch the notification for the user  for the accepted or rejected demand in Achat mode:
    
    notification=DossierAchat.objects.filter(client=request.user,verification__in=['accepté','rejeté'],mysignature='not yet')
    count_notification=notification.count()
    #getting the demandes:
    demande=get_object_or_404(DossierAchat,id=id,verification='rejeté',mysignature='not yet')
    
    #when we click on this page we have to remove the notification by changing msignaturer not yet to signé:
    demande.mysignature="signé"
    demande.save()
    
    context={
        'demande':demande,
        'notification':notification,
        'count_notification': count_notification
    }
    return render(request,'rejected_notification.html',context)        

# here the user check the raison why the demand is rejected or accepted in Achat mode:
def check_raison(request, id):
       
    notification=DossierAchat.objects.filter(client=request.user,verification__in=['accepté','rejeté'],mysignature='not yet')
    count_notification=notification.count()
    #getting the demandes:
    demande=get_object_or_404(DossierAchat,id=id,verification__in=['rejeté','accepté'],mysignature='signé')
    
    context={
        'demande':demande,
        'notification':notification,
        'count_notification': count_notification
    }
    return render(request,'check_raison.html',context) 