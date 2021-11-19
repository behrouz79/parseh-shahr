from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from .models import Product, Comment, Sell, Category
from .forms import CommentForm


class AllProduct(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 30
    extra_context = {
        'title': 'محصولات',
        'categories': Category.objects.all()
    }
    ordering = ('-id',)

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        search = self.request.GET.get('search', None)
        if category is not None:
            return Product.objects.filter(category__slug=category, stock__gte=0)
        elif search is not None:
            return Product.objects.filter(title=search, stock__gte=0)
        else:
            return Product.objects.filter(stock__gte=0)


class DetailProduct(FormMixin, DetailView):
    model = Product
    form_class = CommentForm
    template_name = 'products/detail.html'
    extra_context = {
        'title': 'جزيیات',
        'most_sell': Sell.objects.order_by('-count')[:5]
    }

    def get_success_url(self):
        return reverse('product:detail', args=[self.object.id, self.object.slug])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.object
            comment.save()
            messages.success(request, 'نظر شما با موقیت ثبت شد و پس از تایید نمایش داده می شود.')
        else:
            messages.error(request, 'مشکلی در ارسال نظر پیش آمده.')
        return super().form_valid(form)


@login_required(redirect_field_name='next')
def remove_comment(request):
    if request.method == "POST":
        id = request.POST['id']
        product = None
        if Comment.objects.filter(id=id).exists():
            c = Comment.objects.get(id=id)
            product = Product.objects.get(id=c.product.id)
            c.delete()
        return redirect('product:detail', product.id, product.slug)

