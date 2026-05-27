from io import BytesIO

import qrcode

from django.core.files import File
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

from .forms import CredentialForm
from .ai_modules.fraud_detection import detect_fraud
from .ai_modules.ocr import extract_text
from .ai_modules.qr_verify import (
    scan_qr,
    extract_qr_from_pdf
)

from .blockchain import Blockchain
from .ethereum import web3
from .models import Credential


blockchain = Blockchain()


def home(request):

    # FORM SUBMISSION
    if request.method == 'POST':

        form = CredentialForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

    else:

        form = CredentialForm()

    credentials = Credential.objects.all()

    # AI VERIFICATION
    for credential in credentials:

        if credential.certificate_file:

            # Skip already verified
            if credential.status == "Approved":
                continue

            if credential.status == "Rejected":
                continue

            # FILE PATH
            file_path = (
                credential.certificate_file.path
            )

            # OCR TEXT EXTRACTION
            text = extract_text(file_path)

            print("OCR TEXT:")
            print(text)

            student_name = (
                credential.student_name.lower()
            )

            ocr_text = text.lower()

            # =========================
            # QR VERIFICATION
            # =========================

            qr_data = None

            # PDF QR SCAN
            if file_path.endswith(".pdf"):

                qr_data = extract_qr_from_pdf(
                    file_path
                )

            # IMAGE QR SCAN
            elif file_path.endswith(
                ('.png', '.jpg', '.jpeg')
            ):

                qr_data = scan_qr(
                    file_path
                )

            print("QR DATA:", qr_data)

            # NO QR FOUND
            if not qr_data:

                credential.status = "Rejected"

                credential.save()

                continue

            # INVALID QR
            if "verify" not in qr_data:

                credential.status = "Rejected"

                credential.save()

                continue

            # =========================
            # STUDENT NAME MATCHING
            # =========================

            if student_name not in ocr_text:

                credential.status = "Rejected"

                credential.save()

                continue

            # =========================
            # FRAUD DETECTION
            # =========================

            is_fake = detect_fraud(text)

            if is_fake:

                credential.status = "Rejected"

                credential.save()

            else:

                credential.status = "Approved"

                # QR CODE GENERATION
                verification_url = (
                    f"http://127.0.0.1:8000/verify/{credential.id}/"
                )

                qr = qrcode.make(
                    verification_url
                )

                buffer = BytesIO()

                qr.save(
                    buffer,
                    format='PNG'
                )

                credential.qr_code.save(
                    f'qr_{credential.id}.png',
                    File(buffer),
                    save=False
                )

                # BLOCKCHAIN STORAGE
                blockchain.add_block(
                    credential.certificate_name
                )

                # ETHEREUM CHECK
                if web3.is_connected():

                    print(
                        "Ethereum Connected"
                    )

                else:

                    print(
                        "Ethereum Connection Failed"
                    )

                # EMAIL NOTIFICATION
                send_mail(
                    subject='Credential Approved',
                    message='Your credential has been approved successfully.',
                    from_email='asbhma.23@gmail.com',
                    recipient_list=[
                        'devadigakeerthi98@gmail.com'
                    ],
                    fail_silently=False,
                )

                credential.save()

    return render(
        request,
        'home.html',
        {
            'credentials': credentials,
            'form': form
        }
    )


def approve_credential(request, id):

    credential = get_object_or_404(
        Credential,
        id=id
    )

    credential.status = "Approved"

    credential.save()

    return render(
        request,
        'success.html',
        {
            'credential': credential
        }
    )


def verify_credential(request, id):

    credential = get_object_or_404(
        Credential,
        id=id
    )

    if credential.status == "Approved":

        result = "Valid Credential"

    else:

        result = "Invalid Credential"

    return render(
        request,
        'verify.html',
        {
            'result': result,
            'credential': credential
        }
    )


def reject_credential(request, id):

    credential = get_object_or_404(
        Credential,
        id=id
    )

    credential.status = "Rejected"

    credential.save()

    return render(
        request,
        'reject.html',
        {
            'credential': credential
        }
    )