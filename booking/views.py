from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import TourPackage, Resort, Booking, Enquiry, Review, HeroBanner, SeasonalBanner, Category, Contact, ClientReview
from .forms import EnquiryForm, ReviewForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

# Home view 
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        destination = request.POST.get('destination')
        contact_number = request.POST.get('number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            full_name=name,
            destination=destination,
            contact_number=contact_number,
            email=email,
            message=message
        )
        return redirect(request.path_info)
    
    packages = TourPackage.objects.all()
    resorts = Resort.objects.all()
    hero_banners = HeroBanner.objects.filter(is_active=True)
    seasonal_banners =  SeasonalBanner.objects.latest('created_at')
    featured_tourpackages = TourPackage.objects.filter(is_featured=True)
    featured_categories = Category.objects.filter(is_featured=True)
    client_reviews = ClientReview.objects.all()

    # Fetch last 5 packages in "North India"
    north_india_category = Category.objects.filter(name="North India").first()
    north_india_packages = []
    if north_india_category:
        north_india_packages = TourPackage.objects.filter(
            category=north_india_category
        ).order_by('-id')[:5]

    south_india_category = Category.objects.filter(name="South India").first()
    south_india_packages = []
    if south_india_category:
        south_india_packages = TourPackage.objects.filter(
            category=south_india_category
        ).order_by('-id')[:5]

    east_india_category = Category.objects.filter(name="East India").first()
    east_india_packages = []
    if east_india_category:
        east_india_packages = TourPackage.objects.filter(
            category=east_india_category
        ).order_by('-id')[:5]

    west_india_category = Category.objects.filter(name="West India").first()
    west_india_packages = []
    if west_india_category:
        west_india_packages = TourPackage.objects.filter(
            category=west_india_category
        ).order_by('-id')[:5]

    return render(request, 'home.html', {
        'packages': packages,
        'resorts': resorts,
        'client_reviews': client_reviews,
        'hero_banners': hero_banners,
        'seasonal_banners': seasonal_banners,
        'featured_tourpackages': featured_tourpackages,
        'featured_categories': featured_categories,
        'north_india_packages': north_india_packages,
        'south_india_packages': south_india_packages,
        'east_india_packages': east_india_packages,
        'west_india_packages': west_india_packages,
    })

# about_us
def about_us_view(request):
    return render(request, 'about_us.html')

# contact_us
def contact_us_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        destination = request.POST.get('destination')
        contact_number = request.POST.get('number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            full_name=name,
            destination=destination,
            contact_number=contact_number,
            email=email,
            message=message
        )
        return redirect(request.path_info)

    return render(request, 'contact_us.html')

# Package detail page
def package_detail_view(request, subcategory_slug, package_slug):
    category = get_object_or_404(Category, slug=subcategory_slug)
    package = get_object_or_404(TourPackage, slug=package_slug, category=category)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('number')

        Enquiry.objects.create(
            name=name,
            email=email,
            contact_number=contact_number,
            related_package=package
        )
        return redirect(request.path_info)

    return render(request, 'india/package_detail.html', {
        'package': package,
        'title_main': package.title.split('–')[0].strip() if '–' in package.title else package.title,
    })

def india_tours_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        destination = request.POST.get('destination')
        contact_number = request.POST.get('number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            full_name=name,
            destination=destination,
            contact_number=contact_number,
            email=email,
            message=message
        )
        return redirect(request.path_info)
    
    india_category = Category.objects.filter(parent_choice='India Tours', parent__isnull=True).first()

    india_subcategories = Category.objects.filter(parent=india_category).annotate(
        package_count=Count('packages'),
        has_children=Count('subcategories')
    )

    # Annotate sub-subcategories with package_count
    for subcat in india_subcategories:
        subcat.children = Category.objects.filter(parent=subcat).annotate(
            package_count=Count('packages')
        )

    return render(request, 'india/destinations.html', {
        'india_subcategories': india_subcategories
    })

def india_subcategory_detail(request, subcategory_slug):
    subcategory = get_object_or_404(Category, slug=subcategory_slug, parent_choice='india')

    # Get child categories of this subcategory
    child_categories = Category.objects.filter(parent=subcategory)

    # Fetch packages for subcategory and its children
    packages = TourPackage.objects.filter(
        Q(category=subcategory) | Q(category__in=child_categories)
    )

    return render(request, 'india/india_subcategory_detail.html', {
        'subcategory': subcategory,
        'packages': packages
    })

def international_tours_view(request):
    if request.method == 'POST':
        Contact.objects.create(
            full_name=request.POST.get('name'),
            destination=request.POST.get('destination'),
            contact_number=request.POST.get('number'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect(request.path_info)

    international_packages = TourPackage.objects.filter(parent_choice='international')

    return render(request, 'international/packages.html', {
        'international_packages': international_packages
    })

def international_package_detail_view(request,package_slug):
    # category = get_object_or_404(Category, slug=subcategory_slug)
    package = get_object_or_404(TourPackage, slug=package_slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('number')

        Enquiry.objects.create(
            name=name,
            email=email,
            contact_number=contact_number,
            related_package=package
        )
        return redirect(request.path_info)  # Reload page or redirect to thank-you

    return render(request, 'international/package_detail.html', {
        'package': package
    })


def ayurveda_tours_view(request):
    if request.method == 'POST':
        Contact.objects.create(
            full_name=request.POST.get('name'),
            destination=request.POST.get('destination'),
            contact_number=request.POST.get('number'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect(request.path_info)

    ayurveda_packages = TourPackage.objects.filter(parent_choice='ayurveda')

    return render(request, 'ayurveda/packages.html', {
        'ayurveda_packages': ayurveda_packages
    })

def ayurveda_package_detail_view(request,package_slug):
    # category = get_object_or_404(Category, slug=subcategory_slug)
    package = get_object_or_404(TourPackage, slug=package_slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('number')

        Enquiry.objects.create(
            name=name,
            email=email,
            contact_number=contact_number,
            related_package=package
        )
        return redirect(request.path_info)  # Reload page or redirect to thank-you

    return render(request, 'ayurveda/package_detail.html', {
        'package': package
    })

# Resort detail page
def resort_detail(request, pk):
    resort = Resort.objects.get(pk=pk)
    return render(request, 'resort_detail.html', {'resort': resort})

# Enquiry form view
def enquiry_view(request):
    packages = TourPackage.objects.all()
    resorts = Resort.objects.all()
    success = False

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        related_package_id = request.POST.get('related_package')
        related_resort_id = request.POST.get('related_resort')

        related_package = TourPackage.objects.filter(id=related_package_id).first() if related_package_id else None
        related_resort = Resort.objects.filter(id=related_resort_id).first() if related_resort_id else None

        enquiry = Enquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            related_package=related_package,
            related_resort=related_resort,
        )

        # send_mail(
        #     'New Enquiry Received',
        #     f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}",
        #     'your_email@example.com',
        #     ['admin@example.com'],
        #     fail_silently=False,
        # )

        success = True

    return render(request, 'enquiry.html', {
        'packages': packages,
        'resorts': resorts,
        'success': success,
    })

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'login.html')

# User logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Booking history view for authenticated users
def booking_history(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking_history.html', {'bookings': bookings})
    return redirect('login')

# Review submission view
def submit_review(request, item_id, item_type):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if item_type == 'package':
                review.package = TourPackage.objects.get(id=item_id)
            else:
                review.resort = Resort.objects.get(id=item_id)
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'submit_review.html', {'form': form})

def search_packages(request):
    query = request.GET.get('q', '')
    packages = TourPackage.objects.filter(title__icontains=query).select_related('category')[:10]

    results = []
    for pkg in packages:
        parent = pkg.parent_choice

        if parent == 'india' and pkg.category:
            url = reverse('package_detail', args=[pkg.category.slug, pkg.slug])
        elif parent == 'international':
            url = reverse('international_package_detail', args=[pkg.slug])
        elif parent == 'ayurveda':
            url = reverse('ayurveda_package_detail', args=[pkg.slug])
        else:
            continue  # Skip 'specials' or any other unknown category

        results.append({
            'title': pkg.title,
            'url': url,
        })

    return JsonResponse({'results': results})