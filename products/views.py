from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'products/home.html')

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url']:
            try:
                im = request.FILES['icon']
                ic = request.FILES['image']
            except Exception:
                return render(request, 'products/create.html', {'error': 'Make sure to upload both icon and image!'})            
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://'+request.POST['url']
            product.pub_date = timezone.datetime.now()
            product.icon = ic
            product.image = im
            product.hunter = request.user
            product.save()
            return redirect('home')
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required'})
    else:
        return render(request, 'products/create.html')