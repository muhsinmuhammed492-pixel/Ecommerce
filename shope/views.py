from django.shortcuts import render
from .models import Product,CartItem,Order
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product, Category,Review
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.db.models import Q
from .models import Order 
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


@login_required(login_url='login')
def CartProduct(request):
    cartitems = CartItem.objects.filter(user=request.user)
    return render(request, 'cartitem.html', {'cartitems': cartitems})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product,id=product_id,is_available=True)
    qty=int(request.POST.get('quantity',1))
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    messages.success(request, "Product added to cart successfully!")
    if not created:
        cart_item.quantity += qty
    else:cart_item.quantity=qty
    cart_item.save()


    return redirect('index')

def Remove_form_cart(request, item_id):
    item=CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart_page')

def update_cart(request, item_id):
    if request.method == 'POST':
        new_qty = request.POST.get('quantity')
        cart_item = CartItem.objects.get(id=item_id)
        if int(new_qty) > 0:
            cart_item.quantity = int(new_qty)
            cart_item.save()
        else:
            cart_item.delete() # ക്വാണ്ടിറ്റി 0 ആക്കിയാൽ ഐറ്റം ഒഴിവാക്കാം
    return redirect('cart_page') # ഇവിടെ urls.py-ൽ കൊടുത്ത name നൽകുക

class SignUpView(CreateView):
    form_class=UserCreationForm
    template_name='registration/signup.html'
    success_url=reverse_lazy('login')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        for field in form.fields.values():
            field.help_text = ""
            
        if 'username' in form.fields:
            form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
            
        if 'password1' in form.fields:
            form.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
            
        if 'password2' in form.fields:
            form.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
            
        return form

class MyLoginView(LoginView):
    template_name='registration/login.html'


def logout_view(request):
    logout(request)
    return redirect('login')


class CheckoutView(LoginRequiredMixin,CreateView):
    model = Order
    fields = ['full_name', 'address', 'city', 'pincode']
    template_name = "checkout.html"
    success_url = reverse_lazy('index')

    def get_initial(self):
        initial = super().get_initial()

        cart_items = CartItem.objects.filter(user=self.request.user)

        total = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        initial['total_amount'] = total  # (optional display only)

        return initial

    def form_valid(self, form):

        form.instance.user = self.request.user

        cart_items = CartItem.objects.filter(
            user=self.request.user,
            order__isnull=True
        )

        total = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        form.instance.total_amount = total

        response = super().form_valid(form)

        # attach cart items to order
        for item in cart_items:
            item.order = self.object
            item.save()

        messages.success(self.request, "Order placed successfully!")

        return response
    
def add_product(request):
    if request.method == "POST":
        title = request.POST.get('title')
        price = request.POST.get('price')
        category_name = request.POST.get('category')

        image = request.FILES.get('image')
        image_url = request.POST.get('image_url')

        category_obj, created = Category.objects.get_or_create(name=category_name)

        Product.objects.create(
            title=title,
            price=price,
            category=category_obj,
            image=image if image else None,
            image_url=image_url if not image else None
        )

        return redirect('index')

    return render(request, 'add_product.html')

def is_superadmin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_superadmin)
def add_product(request):
    return render(request, "add_product.html")


def search_view(request):
    query = request.GET.get('query')
    results = []
    if query:
        # പ്രൊഡക്റ്റ് ടൈറ്റിലിലോ കാറ്റഗറിയിലോ തിരയുന്നു
        results = Product.objects.filter(
    Q(title__icontains=query) | Q(category__name__icontains=query)
)
        
    return render(request, 'search_results.html', {'results': results, 'query': query})


@login_required(login_url='login')
def product_detail(request, pk):
    # pk ഉപയോഗിച്ച് പ്രൊഡക്റ്റ് എടുക്കുന്നു, ഇല്ലെങ്കിൽ 404 എറർ കാണിക്കും
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def add_review(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            product=product,
            user=request.user,
            rating=int(rating),
            comment=comment
        )
        return redirect('product_detail', pk=product_id)


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('cartitem_set__product')

    context = {
        'orders': orders
    }

    return render(request, 'my_orders.html', context)

def category_products(request, name):
    products = Product.objects.filter(category__name=name)

    return render(request, 'category.html', {
        'products': products,
        'category_name': name
    })