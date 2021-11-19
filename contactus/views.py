from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContactUsForm
from .models import ContactUs as ModelContactUs


class ContactUs(CreateView):
    template_name = 'contactus/contactus.html'
    model = ModelContactUs
    form_class = ContactUsForm
    extra_context = {
        'title': 'تماس با ما'
    }
    success_url = reverse_lazy('contactus:contactus')

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.sender = self.request.user
        contact.save()
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد , پاسخ برای ایمیل ثبت شده حساب شما ارسال میشود.')
        return super(ContactUs, self).form_valid(form)
