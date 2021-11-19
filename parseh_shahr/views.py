from django.shortcuts import render
from aboutus.models import AboutUs as ModelAboutUs
from products.models import Category


def header(request):
    context = {
        'categories': Category.objects.all(),
        'title': 'موبایل پارسه شهر',
        'head': 'محصولات',
        'contact': ModelAboutUs.objects.filter().first(),
    }
    return render(request, 'shared/header.html', context)


def footer(request):
    context = {
        'categories': Category.objects.all(),
        'contact': ModelAboutUs.objects.filter().first(),
    }
    return render(request, 'shared/footer.html', context)

