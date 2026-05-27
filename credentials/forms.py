from django import forms

from .models import Credential


class CredentialForm(forms.ModelForm):

    class Meta:

        model = Credential

        fields = [
            'student_name',
            'certificate_name',
            'certificate_file'
        ]