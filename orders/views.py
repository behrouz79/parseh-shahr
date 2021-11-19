from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from products.models import Product
from django.contrib import messages
from .models import Order as ModelOrder


class Order(TemplateView):
    template_name = 'orders/order.html'
    extra_context = {
        'title': 'سبد خرید فعال',
    }


class CompleteOrder(TemplateView):
    template_name = 'orders/checkout_complete.html'
    extra_context = {
        'title': 'سبد خرید فعال',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['refid'] = ModelOrder.objects.filter(owner=self.request.user, is_paid=True).last().refid
        return context


@login_required(redirect_field_name='next')
@require_POST
def add_order(request, id):
    order = ModelOrder.objects.filter(owner=request.user, is_paid=False).first()
    if order is None:
        order = ModelOrder.objects.create(owner=request.user, is_paid=False)
    product = get_object_or_404(Product, id=id)
    count = 1
    if order.orderdetailorder.filter(product=product).exists():
        ord = order.orderdetailorder.get_queryset().get(product=product)
        if product.stock < ord.count +1:
            messages.error(request, 'موجودی محصول برای خرید به پایان رسیده.')
        else:
            ord.count += 1
            ord.save()
            count = ord.count
            messages.success(request, f'{count} مورد از این محصول در سبد شما موجود شد.')
    else:
        order.orderdetailorder.create(product=product, price=int(product.amount - (product.amount * (product.discounted / 100))), count=count)

    return redirect(product)


@login_required(redirect_field_name='next')
@require_GET
def plus_order(request, id):
    order = ModelOrder.objects.filter(owner=request.user, is_paid=False).first()
    product_count = Product.objects.get(id=id).stock
    pro = order.orderdetailorder.get_queryset().get(product__id=id)
    if product_count == pro.count:
        messages.error(request, 'موجودی محصول برای خرید به پایان رسیده.')
        return redirect('order:active')
    pro.count += 1
    pro.save()
    return redirect('order:active')


@login_required(redirect_field_name='next')
@require_GET
def minus_order(request, id):
    order = ModelOrder.objects.filter(owner=request.user, is_paid=False).first()
    pro = order.orderdetailorder.get_queryset().get(product_id=id)
    if pro.count == 0 or pro.count == 1:
        messages.error(request, 'برای حذف محصول از گزینه ضربدر استقاده کنید.')
        return redirect('order:active')
    pro.count -= 1
    pro.save()
    return redirect('order:active')


@login_required(redirect_field_name='next')
@require_GET
def remove_order(request, id):
    order = ModelOrder.objects.filter(owner=request.user, is_paid=False).first()
    pro = order.orderdetailorder.get_queryset().get(product_id=id)
    pro.delete()
    return redirect('order:active')

