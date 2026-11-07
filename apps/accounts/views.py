from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout, get_user_model
from .forms.registrationForm import RegisterForm,admin_register_userForm
from .forms.loginForm import LoginForm
from .forms.info_modificationForm import InfoModificationForm 
from .forms.resetpassForm import PasswordResetForm
from .forms.forgotten_set_passwordForm import SetPasswordForm   
from .models import User
from apps.dossiers.models import DossierAchat
from apps.location.models import DossierLocation
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from decimal import Decimal
#the built in django PasswordChangeForm is used to change the password of the user:
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash

# sending email to the user email account after registration
def mailactive(request, user, to_email):
    mail_subject = 'Welcome to Mmotors.'

    messagetemplate = render_to_string('activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(
        subject=mail_subject,
        body=messagetemplate,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )

    email.content_subtype = "html"

    try:
        result = email.send(fail_silently=False)
        print("Résultat envoi email :", result)

        if result == 1:
            messages.success(
                request,
                "Un email de confirmation a été envoyé. Vérifiez votre boîte de réception et vos spams."
            )
        else:
            messages.error(request, "L'email de confirmation n'a pas pu être envoyé.")

    except Exception as e:
        print("ERREUR ENVOI EMAIL :", str(e))
        messages.error(request, "Erreur lors de l'envoi de l'email de confirmation.")
# Activate user account after clicking in the link sent to email
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('core:home')
        
# registration view
def registration(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hachage du mot de passe
            user.set_password(form.cleaned_data['password'])
            
            user.is_active = False
            user.save()
            mailactive(request, user, form.cleaned_data.get('email'))
            # Send welcome email
           
            #login(request, user) this will log in the user directly after registration
            return redirect('accounts:success')#redirect to success page after registration to inform user to check email for verification link
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})     

# here admin try to register a user with the role
def admin_user_registration(request):
    
    #getting all pending demande d achat  for the admin and count them:
    dossier=DossierAchat.objects.filter(verification ="pending...")
    count=dossier.count()
    
    #get all new booking car demande:    
    booking_pending = DossierLocation.objects.filter(status="encours")
    count_booking_pending=booking_pending.count()
    
    if request.method == 'POST':
        form = admin_register_userForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True  # Set the user as staff
            user.save()
            messages.success(request,"Vous venez d'ajouter un utilisateur avec succès")
    else:
        form = admin_register_userForm()
        
    context={
        'form': form,
        'count': count,
        'dossier':dossier,
        'booking_pending':booking_pending,
        'count_booking_pending':count_booking_pending,
    }    
    return render(request, 'administration/add_user.html', context)  

#admin delete all user:
def delete_all_user(request):
    User.objects.all().delete()
    messages.success(request, "All users have been deleted successfully.")
    return redirect('core:admin_manage_user')  # Redirect to the admin manage user page after deletion

#login view
def login_view(request):
    
    # Create an instance of the form
    form = LoginForm(request.POST or None)
    error = None
    
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        #Check if user exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None

        if user_obj is None:
            error = "Email or password is incorrect"

        elif not user_obj.is_active:  # si le compte is active == False il est bloqué
            error = "Your account is blocked please contact support for more information to :testeden8@gmail.com"

        else:
            #Now authenticate password
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('core:home')  # Redirect to the home page after successful login
            else:
                error = "Email or password is incorrect"

    return render(request, 'login.html', {'form': form, 'error': error})
    
#logout view
def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Redirect to the login page after logout

#success page after registration to inform user to check email for verification link
def success(request):
    return render(request, 'success.html')

#failed registration page after registation to inform user that registration failed
def failed(request):
    return render(request, 'failed.html')

#success_registration to login after successful registration the verification link is clicked and account is activated
def success_registration(request):
    return render(request, 'success_registration.html')

#failed_registration to inform user that registration failed the verification link is not clicked and account is not activated
def failed_registration(request):
    return render(request, 'failed_registration.html')

#user profile view
def user_profil(request):
   
    # get the current user:   
    user= User.objects.filter(id=request.user.id).first()
    
    #notification for user check if the user dossier to buy a car has been accepted: he has to sign the contract
    notification=DossierAchat.objects.filter(client=request.user,verification__in=['accepté','rejeté'],mysignature='not yet')
    count_notification=notification.count()
           
    #getting all location or booking notification for the user:
    notification_location=DossierLocation.objects.filter(client=request.user,status__in=['accepté','rejeté'],mysignature='not yet')
    count_notification_location=notification_location.count()
    
    #taking all request achat de dossier pour cet utilisateur:
    dossiers=DossierAchat.objects.filter(client=user)
    count_dossier=dossiers.count()
    
    #taking the request booking for this user:
    bookings=DossierLocation.objects.filter(client=user).count()
    #ici on check if one of your dossier is accepted and you have to signe the contract of buying
    #to make appear the notification sign for the user:
    notification=DossierAchat.objects.filter(client=request.user,verification ='accepté',mysignature='not yet')
    count_notification=notification.count()
    
    context={
       'user':user,
       'dossiers':dossiers,
       'notification':notification,
       'count_notification':count_notification,
       'count_dossier':count_dossier,
       'bookings':bookings,
       'notification_location':notification_location,
       'count_notification_location':count_notification_location
    }
    return render(request, 'profil/index.html',context)

# user information
@login_required
def user_info(request):
   
    user= User.objects.filter(id=request.user.id).first()
    
    #ici on check if one of your dossier is accepted and you have to signe the contract of buying
    #to make appear the notification sign for the user:
    notification=DossierAchat.objects.filter(client=request.user,verification ='accepté',mysignature='not yet')
    count_notification=notification.count()
    
    context={
       'user':user,
       'notification':notification,
       'count_notification':count_notification
    }
    return render(request, 'profil/user_info.html',context)

# getting user all request achat
@login_required
def user_all_request(request):
   
    # on recupere l utilisateur connecté:   
    user= User.objects.filter(id=request.user.id).first()
    
    #taking all request de dossier pour cet utilisateur order by descending:
    contract=DossierAchat.objects.filter(client=user).order_by('-id')
    
    #ici on check if one of your dossier is accepted and you have to signe the contract of buying
    #to make appear the notification sign for the user:
    notification=DossierAchat.objects.filter(client=request.user,verification ='accepté',mysignature='not yet')
    count_notification=notification.count()
    
    context={
       'user':user,
       'notification':notification,
       'count_notification':count_notification,
       'contract':contract,
    }
    return render(request, 'profil/request_user.html',context)

@login_required
def user_location_request(request):
   
    # on recupere l utilisateur connecté:   
    user= request.user
    
    #taking all location request de dossier pour cet utilisateur:
    contract=DossierLocation.objects.filter(client=user).order_by('-id')
    
    # am looping to get each days of booking and the price:
    for demande in contract:

        days = (
            demande.date_retour - demande.date_depart
        ).days

        price = Decimal(str(demande.vehicule.prix))

        demande.days = days
        demande.total = price * days
    
    #ici on check if one of your dossier is accepted and you have to signe the contract of buying
    #to make appear the notification sign for the user for achat:
    notification=DossierAchat.objects.filter(client=request.user,verification ='accepté',mysignature='not yet')
    count_notification=notification.count()
    
    #notification for location to sign if the demande is accepted:
    notification_location=DossierLocation.objects.filter(client=user,status ='accepté',mysignature='not yet')
    count_notification_location=notification.count()
    
    
    context={
       'user':user,
       'notification':notification,
       'count_notification':count_notification,
       'contract':contract,
       'notification_location':notification_location,
       'count_notification_location':count_notification_location,
    }
    return render(request, 'profil/user_location_request.html',context)


#change password view with the django built-in PasswordChangeForm
@login_required
def change_password(request):
    
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            # Prevent logout after password change
            update_session_auth_hash(request, user)

            return redirect("accounts:user_profil")  # Redirect to the user profile page after successful password change
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "profil/change_password.html", {
        "form": form
    })
    
@login_required
def info_modification(request):
    user = request.user
    if request.method == 'POST':
        form = InfoModificationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated successfully.')
            return redirect('accounts:user_profil')
    else:
        form = InfoModificationForm(instance=user)

    return render(request, 'profil/info_modification.html', {'form': form}) 

#forgotten password view password oublié 
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        We've emailed you instructions for setting your password,
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('accounts:sent_mail_reset_password')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="form_forgotten_password.html", 
        context={"form": form}
        )
# sent mail success to reset the password for the forgotten password view
def sent_mail_reset_password(request):
    return render(request, 'sent_mail_reset_password.html')    
    
# confirm the password reset link sent to email to click and reset password
def password_reset_confirm(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is None or not account_activation_token.check_token(user, token):
        messages.error(request, "This password reset link has expired or is invalid.")
        return redirect("core:home")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your password has been reset successfully. You can now log in."
            )
            return redirect("accounts:login")
    else:
        form = SetPasswordForm(user)

    return render(
        request,
        "change_forgotten_password.html",
        {"form": form},
    )