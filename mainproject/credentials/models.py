from django.db import models


class Authority(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Credential(models.Model):

    student_name = models.CharField(max_length=100)

    certificate_name = models.CharField(max_length=200)

    approved_count = models.IntegerField(default=0)

    status = models.CharField(
        max_length=50,
        default="Pending"
    )

    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )

    certificate_file = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    def __str__(self):

        return self.student_name