import os

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from datetime import datetime
from pathlib import Path

def invoice(demandes):

    image_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "img",
        "logo.png"
    )

    if os.path.exists(image_path):
        image_url = Path(image_path).resolve().as_uri()
    else:
        image_url = None

    html = render_to_string(
        "pdf/invoice.html",
        {
            "demandes": demandes,
            "date": datetime.now(),
            "logo_path": image_url,
        }
    )

    pdf = HTML(
        string=html,
        base_url=settings.BASE_DIR,
    ).write_pdf()

    filename = f"contract_{demandes.id}.pdf"

    demandes.facture_pdf.save(
        filename,
        ContentFile(pdf),
        save=True,
    )
    
def invoice_location(demandes,payer,days):

    image_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "img",
        "logo.png"
    )

    if os.path.exists(image_path):
        image_url = Path(image_path).resolve().as_uri()
    else:
        image_url = None

    html = render_to_string(
        "pdf/invoice_location.html",
        {
            "demandes": demandes,
            "payer":payer,
            "days":days,
            "date": datetime.now(),
            "logo_path": image_url,
        }
    )

    pdf = HTML(
        string=html,
        base_url=settings.BASE_DIR,
    ).write_pdf()

    filename = f"contract_{demandes.id}.pdf"

    demandes.facture_pdf.save(
        filename,
        ContentFile(pdf),
        save=True,
    )    