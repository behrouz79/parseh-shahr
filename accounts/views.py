from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from orders.models import Order
from .forms import UserLoginForm, UserRegisterForm


def login_register_user(request):
    if request.user.is_authenticated:
        return redirect('product:all_product')
    next_url = request.GET.get('next', None)
    login_form = UserLoginForm(request.POST or None)
    register_form = UserRegisterForm(request.POST or None)
    if login_form.is_valid():
        user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            messages.success(request, "شما با موفقیت وارد حساب کاربری خود شدید.")
            if next_url:
                return redirect(next_url)
            return redirect('product:all_product')
        messages.error(request, "کاربری یا این مشخصات یافت نشد.")
    if register_form.is_valid():
        c = register_form.cleaned_data
        user = User.objects.create_user(c['username'], c['email'], c['password2'])
        login(request, user)
        messages.success(request, "شما با موفقیت حساب کاربری خود را ایجاد کردید.")
        return redirect('product:all_product')
    return render(request, 'accounts/login-signup.html', {'title': 'ورود / ثبت نام', 'login_form': login_form, 'register_form':register_form})


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('product:all_product')
    logout(request)
    messages.success(request, "شما با موفقیت حساب کاربری خود را ترک کردید.")
    return redirect('product:all_product')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account-info.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حساب کاربری'
        return context


class OrderHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/order_history.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تاریخچه سفارشات'
        context['oldorder'] = Order.objects.filter(owner=self.request.user, is_paid=True).order_by('payment_date')
        return context
