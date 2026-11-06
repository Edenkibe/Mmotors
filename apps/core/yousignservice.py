import logging

import requests
from django.conf import settings
from django.http import JsonResponse
import json
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class YousignClient:

    def __init__(self):
        self.base_url = settings.YOUSIGN_BASE_URL
        self.api_key = settings.YOUSIGN_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def _request(self, method, url, **kwargs):
        if not self.base_url or not self.api_key:
            raise RuntimeError("YouSign is not configured. Please check YOUSIGN_API_KEY and YOUSIGN_BASE_URL.")

        headers = kwargs.pop("headers", {}) or {}
        merged_headers = {**self.headers, **headers}
        response = requests.request(method, url, timeout=30, headers=merged_headers, **kwargs)

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            detail = self._extract_error_detail(response)
            message = f"YouSign API error: {response.status_code} {response.reason}"
            if detail:
                message = f"{message} - {detail}"
            logger.error(message)
            raise RuntimeError(message) from exc

        return response

    def _extract_error_detail(self, response):
        try:
            payload = response.json()
        except ValueError:
            return response.text.strip()

        if isinstance(payload, dict):
            for key in ("message", "error", "detail", "errors"):
                value = payload.get(key)
                if value:
                    if isinstance(value, list):
                        return ", ".join(str(item) for item in value)
                    return str(value)
            return str(payload)

        return str(payload)

    #generation de contrat avec weazy print for achat and location type
    def generate_contract(self, demande, contract_type):
    
        image_path = os.path.join(
            settings.BASE_DIR,
            'static',
            'img',
            'logo.png'
        )

        image_url = (
            Path(image_path).resolve().as_uri()
            if os.path.exists(image_path)
            else None
        )


        if contract_type == "achat":
            template = "pdf/contrat.html"

        elif contract_type == "location":
            template = "pdf/contrat_location.html"

        else:
            raise ValueError("Unknown contract type")


        html = render_to_string(
            template,
            {
                "demandes": demande,
                "date": datetime.now(),
                "logo_path": image_url,
            }
        )


        pdf = HTML(string=html).write_pdf()


        filename = f"contract_{demande.id}.pdf"

        demande.contrat_pdf.save(
            filename,
            ContentFile(pdf),
            save=True,
        )
    #create the signature for achat and location
    def create_signature_request(self, demande, contract_type):

        url = f"{self.base_url}/signature_requests"


        if contract_type == "achat":

            name = f"contrat voiture {demande.vehicule.marque}"
            external_id = f"achat-{demande.id}"


        elif contract_type == "location":

            name = f"contrat location {demande.vehicule.marque}"
            external_id = f"location-{demande.id}"


        else:
            raise ValueError("Unknown contract type")


        payload = {
            "name": name,
            "delivery_mode": "email",
            "external_id": external_id,
        }
        print("YOUSIGN PAYLOAD:", payload)

        response = self._request(
            "post",
            url,
            json=payload
        )

        return response.json()
    
    
    #upload document to yousign:
    def upload_document(self, signature_request_id, file_path):

        url = (
            f"{self.base_url}/signature_requests/"
            f"{signature_request_id}/documents"
        )

        with open(file_path, "rb") as pdf:

            files = {
                "file": (
                    "contrat.pdf",
                    pdf,
                    "application/pdf"
                )
            }

            data = {
                "nature": "signable_document",
                "name": "Contrat voiture"
            }

            response = self._request(
                "POST",
                url,
                files=files,
                data=data
            )

        return response.json()
    # add le signature:
    def add_signer(self, request_id,document_id, first_name, last_name, email):
        if not email or "@" not in email:
           raise ValueError("Customer email is missing or invalid")
        url = (
            f"{self.base_url}/signature_requests/"
            f"{request_id}/signers"
        )

        payload = {
            "info": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "locale": "en",
            },
            "signature_level": "electronic_signature",
            "signature_authentication_mode": "no_otp",
            "fields": [
                {
                    "document_id": document_id,
                    "type": "signature",
                    "page": 1,
                    "x": 100,
                    "y": 700,
                    "width": 180,
                    "height": 40,
                }
            ]
        }
        
        print("ADD SIGNER URL:", url)
        print("ADD SIGNER PAYLOAD:", payload)
        response = self._request("post", url, json=payload)

        print("ADD SIGNER RESPONSE:", response.status_code)
        print("ADD SIGNER BODY:", response.text)
        return response.json()

 
    #to activate the document and the user will receive the email automatically to yousign    
    def activate(self, signature_request_id):
        response = self._request(
            "post",
            f"{self.base_url}/signature_requests/{signature_request_id}/activate",
        )
        return response.json()
      
    
    #download the pdf signed
    def download_signed_document(self,signature_request_id):
        response = self._request(
            "get",
           f"{self.base_url}/signature_requests/{signature_request_id}/documents/download"
        )

        return response.content    
     