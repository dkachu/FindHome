from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout
from .models import House, ContactMessage, CompanyProfile


def index(request):
   
    house_list = House.objects.filter(is_published=True).prefetch_related('gallery').order_by('-list_date')
    
    # 2. Pagination Setup
    # Adjust '12' to change how many properties show per page
    paginator = Paginator(house_list, 12) 
    page_number = request.GET.get('page')
    houses = paginator.get_page(page_number)

    context = {
        'houses': houses, 
    }
    return render(request, 'kiota/index.html', context)


def detail(request, house_id):
   
    house = get_object_or_404(House, pk=house_id)
   
    gallery = house.gallery.all() 
    context = {'house': house, 'gallery': gallery}
    return render(request, 'kiota/detail.html', context)


def about(request):
    return render(request, 'kiota/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_body = request.POST.get('message')

        # Save inquiry to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_body
        )

        messages.success(request, "Your message has been received! Our team will get back to you soon.")
        return redirect('contact')

    return render(request, 'kiota/contact.html')

# 🛡️ Admin: Superuser Dashboard
@login_required
@user_passes_test(lambda u: u.is_superuser)
def owner_dashboard(request):
   
    total_houses = House.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    
    context = {
        'total_houses': total_houses,
        'unread_messages': unread_messages,
        'recent_messages': recent_messages,
    }
    return render(request, 'kiota/owner_dashboard.html', context)


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')
