from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orderuser', verbose_name='خریدار')
    is_paid = models.BooleanField(verbose_name='پرداخت شده / نشده')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
    refid = models.CharField(max_length=200, blank=True, null=True, verbose_name='شماره پیگیری')
    price = models.CharField(max_length=100, blank=True, null=True, verbose_name='قیمت')
    down = models.BooleanField(default=False, verbose_name='فرستاده شده')
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ساخت سبد')
    FullName = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام کامل')
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='شماره تلفن')
    ostan = models.CharField(max_length=50, blank=True, null=True, verbose_name='استان')
    sharestan = models.CharField(max_length=50, blank=True, null=True, verbose_name='شهرستان')
    FullAddress = models.TextField(blank=True, null=True, verbose_name='آدرس کامل')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def get_total_price(self):
        total = 0
        for item in self.orderdetailorder.all():
            total += item.get_total_price()
        return total

    def get_total_discounted_price(self):
        total = 0
        for item in self.orderdetailorder.all():
            total += item.get_total_discounted()
        return total

    def get_count(self):
        return len(self.orderdetailorder.all())

    def __str__(self):
        return self.owner.username


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderdetailorder', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productorderdetailorder', verbose_name='محصول')
    price = models.IntegerField(verbose_name='قیمت')
    count = models.IntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'جزییات سبد خرید'

    def get_total_price(self):
        return self.price * self.count

    def get_total_discounted(self):
        return (self.product.amount * (self.product.discounted / 100)) * self.count

    def __str__(self):
        return f'{self.order}-{self.product.title}'
