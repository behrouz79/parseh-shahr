from django.db import models


class AboutUs(models.Model):
    image = models.ImageField(upload_to='aboutus/')
    text = models.TextField()
    location = models.CharField(max_length=300, blank=True, null=True)
    smartphone = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    sms1 = models.CharField(max_length=30, blank=True, null=True)
    sms2 = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    telegram = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    whatsapp = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'دباره ما'
        verbose_name_plural = 'درباره ما'

    def __str__(self):
        return self.text[:30]
