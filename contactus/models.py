from django.conf import settings
from django.db import models


class ContactUs(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='فرستنده')
    name = models.CharField(max_length=50, verbose_name='نام')
    title = models.CharField(max_length=100, verbose_name='موضوع')
    email = models.CharField(max_length=50, verbose_name='ایمیل')
    description = models.TextField(verbose_name='متن')
    date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    seen = models.BooleanField(default=False, verbose_name='خوانده شده / نشده')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'


