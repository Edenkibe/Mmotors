from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from apps.contact.forms.contactForm import ContactDossierForm


# after the user submite the contact form, this function will send an email to the admin with the details:
def send_contact_email(contact, to_email):

    mail_subject = "New dossier contact request"

    message_template = render_to_string(
        "contact_email.html",
        {
            "contact": contact,
        }
    )

    email = EmailMessage(
        mail_subject,
        message_template,
        to=[to_email],
    )
    email.content_subtype = "html" # this render the email as html without html tags:
      
    return email.send()

# here to contact the admin
def contact_dossier(request):

    if request.method == "POST":

        form = ContactDossierForm(request.POST)

        if form.is_valid():

            contact = form.save()

            send_contact_email(
                contact,
                "testeden8@gmail.com"
            )

            messages.success(
                request,
                "Votre message a bien été envoyé."
            )

            return redirect("contact:success_page")

    else:
        form = ContactDossierForm()


    return render(
        request,
        "index.html",
        {
            "form": form
        }
    )
    
def success_page(request):
    return render(request, "success_page.html")    
    

