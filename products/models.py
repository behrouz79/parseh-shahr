import os
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='عنوان در url')
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE,
        verbose_name='دسته بندی اصلی'
    )

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت')
    slug = models.SlugField(max_length=50, blank=True, null=True, allow_unicode=True, verbose_name='عنوان در url')
    stock = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='موجودی')
    image = models.ImageField(upload_to='product/', verbose_name='تصویر اصلی')
    gallory = models.ManyToManyField('Image', verbose_name='تصاویر گالری')
    active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    discounted = models.IntegerField(default=0, blank=True, null=True, verbose_name='تخفیف')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی ها')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.id, self.slug])

    def collect_discounted(self):
        return int(self.amount - (self.amount * (self.discounted/100)))

    def get_active_comment(self):
        return self.commentproduct.filter(active=True)

    def __str__(self):
        return self.title


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{uuid.uuid1()}{ext}"
    return f"products/{final_name}"


class Image(models.Model):
    image = models.ImageField(upload_to=upload_image_path)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="commentproduct", null=True, blank=True)
    text = models.TextField()
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class Sell(models.Model):
    target = models.OneToOneField(Product, on_delete=models.DO_NOTHING, related_name='product_sell', verbose_name='محصول')
    count = models.IntegerField(default=0, verbose_name='تعداد فروش رفته')

    class Meta:
        ordering = ('-count',)
        verbose_name = 'فروش'
        verbose_name_plural = 'اجناس فروش رفته'
