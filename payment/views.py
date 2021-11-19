from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from zeep import Client
from orders.models import Order
from django.contrib import messages
from products.models import Sell

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "خرید از فروشگاه موبایل پارسه شهر"  # Required
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify'


@login_required(redirect_field_name='next')
@require_POST
def send_request(request):
    open_order: Order = get_object_or_404(Order, owner=request.user, is_paid=False)
    if address(request, open_order):
        amount = open_order.get_total_price()
        if amount < 50000:
            messages.error(request, 'مبلغ خرید شما کمتر از حد مجاز است.')
            return redirect('order:active')
        result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, f"{CallbackURL}/{open_order.id}")
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    messages.error(request, 'اطلاعات ادرس را به درستی وارد کنید.')
    return redirect('order:active')


@login_required(redirect_field_name='next')
def verify(request, id):
    if request.GET.get('Status') == 'OK':
        open_order: Order = get_object_or_404(Order, id=id)
        amount = open_order.get_total_price()
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            open_order.is_paid = True
            open_order.refid = str(result.RefID)
            open_order.payment_date = datetime.now()
            open_order.price = str(amount)
            for item in open_order.orderdetailorder.all():
                sell_option = Sell.objects.filter(target=item.product).first()
                if sell_option is None:
                    sell_option = Sell.objects.create(target=item.product)
                sell_option.count += item.count
                sell_option.save()
                item.product.stock -= item.count
            open_order.save()
            return redirect('order:complete_order')
        elif result.Status == 101:
            return redirect('order:active')
        else:
            return redirect('order:active')
    else:
        return redirect('order:active')


def address(request, open_order):
    try:
        fullname = request.POST['name']
        ostan = request.POST['ostan']
        city = request.POST['city']
        number = request.POST['number']
        fulladdress = request.POST['fulladdress']
        open_order.FullName = fullname
        open_order.ostan = ostan
        open_order.sharestan = city
        open_order.phone = number
        open_order.FullAddress = fulladdress
        open_order.save()
        return True
    except:
        return False