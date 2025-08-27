from django.shortcuts import render, get_object_or_404, redirect
from .decorators import superuser_required
from django.utils.timezone import now
from django.utils.text import slugify
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from booking.models import Category, TourPackage, Booking, Enquiry, Contact, HeroBanner, SeasonalBanner, ClientReview
from booking.forms import CategoryForm, TourPackageForm, BookingForm, EnquiryForm, ContactForm, HeroBannerForm, SeasonalBannerForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'adminpanel/login.html')


def logout_view(request):
    logout(request)
    return redirect('admin_login')

@superuser_required
@login_required(login_url='admin_login')
def admin_dashboard(request):
    three_days_ago = now() - timedelta(days=3)

    total_enquiry = Enquiry.objects.count()
    total_packages = TourPackage.objects.count()
    new_enquiry = Enquiry.objects.filter(created_at__gte=three_days_ago).count()
    recommended_packages = TourPackage.objects.filter(is_featured=True).count()
    enquiry_list = Enquiry.objects.select_related('related_package').order_by('-created_at')

    context = {
        'package_count': total_packages,
        'recommended_package_count': recommended_packages,
        'enquiry_count': total_enquiry,
        'new_enquiry_count': new_enquiry,
        'enquiry_list': enquiry_list,
    }
    return render(request, 'adminpanel/dashboard.html', context)

# Category
@login_required(login_url='admin_login')
def category_list(request):
    items = Category.objects.all().order_by('-id')  # Optional: show latest first
    paginator = Paginator(items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'adminpanel/category_list.html', {'categories': page_obj})

@login_required(login_url='admin_login')
def category_create(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryname')
        tittle_first = request.POST.get('tittlefirst')
        tittle_second = request.POST.get('tittlesecond')
        parent_id = request.POST.get('parentCategory') or None
        parent_choice = request.POST.get('parentChoice')
        short_description = request.POST.get('shortDesc')
        long_description = request.POST.get('longDesc')
        content_first = request.POST.get('contentfir')
        content_second = request.POST.get('contentsec')
        is_featured = request.POST.get('recomanded') == 'on'
        banner_image = request.FILES.get('bannerImage')
        card_image = request.FILES.get('card_image')

        Category.objects.create(
            name=category_name,
            tittle_first=tittle_first,
            tittle_second=tittle_second,
            parent_id=parent_id,
            parent_choice=parent_choice,
            short_description=short_description,
            long_description=long_description,
            content_first=content_first,
            content_second=content_second,
            banner_image_desktop=banner_image,
            card_image=card_image,
            is_featured=is_featured
        )
        return redirect('admin_category_list')

    parent_categories = Category.objects.all()
    return render(request, 'adminpanel/category_form.html', {
        'parent_categories': parent_categories
    })

@login_required(login_url='admin_login')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Use static PARENT_CHOICES from the model
    parent_choices = Category.PARENT_CHOICES

    parent_categories = Category.objects.exclude(pk=category.pk)

    if request.method == 'POST':
        category.name = request.POST.get('categoryName')
        category.tittle_first = request.POST.get('tittlefirst')
        category.tittle_second = request.POST.get('tittlesecond')
        parent_id = request.POST.get('parentCategory') or None
        category.parent_id = parent_id

        category.short_description = request.POST.get('shortDesc')
        category.long_description = request.POST.get('longDesc')
        category.content_first = request.POST.get('contentfir')
        category.content_second = request.POST.get('contentsec')
        category.parent_choice = request.POST.get('parentChoice')  # save the selected one

        category.is_featured = request.POST.get('recomanded') == 'on'

        if request.FILES.get('bannerImage'):
            category.banner_image_desktop = request.FILES['bannerImage']

        category.save()
        return redirect('admin_category_list')

    return render(request, 'adminpanel/category_update.html', {
        'category': category,
        'parent_categories': parent_categories,
        'parent_choices': parent_choices,  # use static choices
        'selected_parent_id': category.parent.id if category.parent else ''
    })



@login_required(login_url='admin_login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('admin_category_list')

# Toggle
@csrf_exempt
def toggle_featured_status(request):
    if request.method == 'POST':
        pkg_id = request.POST.get('id')
        is_featured = request.POST.get('is_featured') == 'true'

        try:
            pkg = TourPackage.objects.get(id=pkg_id)
            pkg.is_featured = is_featured
            pkg.save()
            return JsonResponse({'success': True})
        except TourPackage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Package not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def toggle_featured_is_active(request):
    if request.method == 'POST':
        banner_id = request.POST.get('id')
        is_active = request.POST.get('is_active') == 'true'

        try:
            banner = HeroBanner.objects.get(id=banner_id)
            banner.is_active = is_active
            banner.save()
            return JsonResponse({'success': True})
        except HeroBanner.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Banner not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# TourPackage
@login_required(login_url='admin_login')
def tourpackage_list(request):
    items = TourPackage.objects.all().order_by('created_at')

    # Filters
    search_query = request.GET.get('search', '').strip()
    type_filter = request.GET.get('type', '')
    featured_filter = request.GET.get('featured', '')

    # Apply search filter
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply type (parent_choice) filter
    if type_filter:
        items = items.filter(parent_choice=type_filter)

    # Apply featured filter
    if featured_filter == 'true':
        items = items.filter(is_featured=True)
    elif featured_filter == 'false':
        items = items.filter(is_featured=False)

    # Optional pagination
    paginator = Paginator(items, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'packages': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
        'featured_filter': featured_filter,
        'parent_choices': TourPackage.PARENT_CHOICES,  # if you have defined it in your model
    }
    return render(request, 'adminpanel/tourpackage_list.html', context)

@login_required(login_url='admin_login')
def tourpackage_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug') or slugify(title)
        tags = request.POST.get('tags')
        short_description = request.POST.get('short_description')
        description = request.POST.get('description')
        location = request.POST.get('location')
        price = request.POST.get('price') or 0
        days = request.POST.get('days') or 0
        nights = request.POST.get('nights') or 0
        category_id = request.POST.get('category')
        parent_choice = request.POST.get('parent_choice') or 'india'
        is_featured = True if request.POST.get('is_featured') == 'on' else False

        image_desktop = request.FILES.get('image_desktop')
        image_mobile = request.FILES.get('image_mobile')
        card_image = request.FILES.get('card_image')

        category = Category.objects.filter(id=category_id).first() if category_id else None

        # Save the TourPackage instance first
        tour_package = TourPackage.objects.create(
            title=title,
            slug=slug,
            short_description=short_description,
            description=description,
            location=location,
            price=price,
            days=days,
            nights=nights,
            image_desktop=image_desktop,
            image_mobile=image_mobile,
            card_image=card_image,
            category=category,
            parent_choice=parent_choice,
            is_featured=is_featured,
        )

        # Add tags after object creation
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            tour_package.tags.add(*tag_list)

        return redirect('admin_tourpackage_list')

    categories = Category.objects.all()
    return render(request, 'adminpanel/tourpackage_form.html', {
        'categories': categories,
        'parent_choices': Category.PARENT_CHOICES
    })

@login_required(login_url='admin_login')
def tourpackage_update(request, pk):
    item = get_object_or_404(TourPackage, pk=pk)

    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.slug = request.POST.get('slug') or slugify(item.title)
        item.short_description = request.POST.get('short_description')
        item.description = request.POST.get('description')
        item.location = request.POST.get('location')

        price = request.POST.get('price')
        item.price = price if price else None

        days = request.POST.get('days')
        item.days = int(days) if days else None

        nights = request.POST.get('nights')
        item.nights = int(nights) if nights else None

        item.is_featured = request.POST.get('is_featured') == 'on'

        category_id = request.POST.get('category')
        if category_id:
            item.category = Category.objects.get(pk=category_id)

        parent_id = request.POST.get('parent_package')
        if parent_id:
            item.parent_package = TourPackage.objects.get(pk=parent_id)

        if request.FILES.get('banner_image_desktop'):
            item.image_desktop = request.FILES['banner_image_desktop']
        if request.FILES.get('banner_image_mobile'):
            item.image_mobile = request.FILES['banner_image_mobile']
        if request.FILES.get('card_image'):
            item.card_image = request.FILES['card_image']

        # Update tags
        tags = request.POST.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            item.tags.set(tag_list)
        else:
            item.tags.clear()

        item.save()
        return redirect('admin_tourpackage_list')

    # Convert tag list to comma-separated string for form field
    existing_tags = ', '.join(tag.name for tag in item.tags.all())

    return render(request, 'adminpanel/tourpackage_update_form.html', {
        'item': item,
        'categories': Category.objects.all(),
        'parent_choices': Category.PARENT_CHOICES,
        'all_packages': TourPackage.objects.exclude(id=item.id),
        'existing_tags': existing_tags
    })

@login_required(login_url='admin_login')
def tourpackage_delete(request, pk):
    item = get_object_or_404(TourPackage, pk=pk)
    item.delete()
    return redirect('admin_tourpackage_list')

# Booking
@login_required(login_url='admin_login')
def booking_list(request):
    items = Booking.objects.all()
    return render(request, 'adminpanel/booking_list.html', {'bookings': items})

@login_required(login_url='admin_login')
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_booking_list')
    return render(request, 'adminpanel/booking_form.html', {'form': form})

@login_required(login_url='admin_login')
def booking_update(request, pk):
    item = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('admin_booking_list')
    return render(request, 'adminpanel/booking_form.html', {'form': form})

@login_required(login_url='admin_login')
def booking_delete(request, pk):
    item = get_object_or_404(Booking, pk=pk)
    item.delete()
    return redirect('admin_booking_list')

# Enquiry
@login_required(login_url='admin_login')
def enquiry_list(request):
    items = Enquiry.objects.all()
    return render(request, 'adminpanel/enquiry_list.html', {'enquiries': items})

@login_required(login_url='admin_login')
def enquiry_detail(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    return render(request, 'adminpanel/enquiry_detail.html', {'enquiry': enquiry})


@login_required(login_url='admin_login')
def contact_enquiry_detail(request, pk):
    contact_qs = get_object_or_404(Contact, pk=pk)
    return render(request, 'adminpanel/contact_details.html', {'contact': contact_qs})


@login_required(login_url='admin_login')
def enquiry_create(request):
    form = EnquiryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_enquiry_list')
    return render(request, 'adminpanel/enquiry_form.html', {'form': form})

@login_required(login_url='admin_login')
def enquiry_update(request, pk):
    item = get_object_or_404(Enquiry, pk=pk)
    form = EnquiryForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('admin_enquiry_list')
    return render(request, 'adminpanel/enquiry_form.html', {'form': form})

@login_required(login_url='admin_login')
def enquiry_delete(request, pk):
    item = get_object_or_404(Enquiry, pk=pk)
    item.delete()
    return redirect('admin_contact_list')

# Contact
@login_required(login_url='admin_login')
def contact_list(request):
    contact_qs = Contact.objects.all().order_by('-id')
    enquiry_qs = Enquiry.objects.all().order_by('-id')

    contact_paginator = Paginator(contact_qs, 10) 
    enquiry_paginator = Paginator(enquiry_qs, 10) 

    contact_page_number = request.GET.get('contact_page')
    enquiry_page_number = request.GET.get('enquiry_page')

    contacts = contact_paginator.get_page(contact_page_number)
    enquiry_items = enquiry_paginator.get_page(enquiry_page_number)

    return render(request, 'adminpanel/enquiry_list.html', {
        'contacts': contacts,
        'enquiry_items': enquiry_items,
    })

@login_required(login_url='admin_login')
def contact_create(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_contact_list')
    return render(request, 'adminpanel/contact_form.html', {'form': form})

@login_required(login_url='admin_login')
def contact_update(request, pk):
    item = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('admin_contact_list')
    return render(request, 'adminpanel/contact_form.html', {'form': form})

@login_required(login_url='admin_login')
def contact_delete(request, pk):
    item = get_object_or_404(Contact, pk=pk)
    item.delete()
    return redirect('admin_contact_list')

# HeroBanner
@login_required(login_url='admin_login')
def hero_banner_list(request):
    items = HeroBanner.objects.all().order_by('-id')
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'adminpanel/hero_banner_list.html', {'banners': page_obj})

@login_required(login_url='admin_login')
def hero_banner_create(request):
    if request.method == 'POST':
        title = request.POST.get('bannerTitle')
        subtitle = request.POST.get('bannerContent')
        image_desktop = request.FILES.get('bannerImage')
        image_mobile = request.FILES.get('mobileBannerImage')

        if title and subtitle and image_desktop:
            HeroBanner.objects.create(
                title=title,
                subtitle=subtitle,
                image_desktop=image_desktop,
                image_mobile=image_mobile
            )
            return redirect('admin_hero_banner_list')
        else:
            error = "All fields are required."
            return render(request, 'adminpanel/hero_banner_form.html', {'error': error})

    return render(request, 'adminpanel/hero_banner_form.html')


@login_required(login_url='admin_login')
def hero_banner_update(request, pk):
    banner = get_object_or_404(HeroBanner, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('bannerTitle')
        subtitle = request.POST.get('bannerContent')
        image_desktop = request.FILES.get('bannerImage')
        image_mobile = request.FILES.get('mobileBannerImage')

        banner.title = title
        banner.subtitle = subtitle

        if image_desktop:
            banner.image_desktop = image_desktop 
        if image_mobile:
            banner.image_mobile = image_mobile 

        banner.save()
        return redirect('admin_hero_banner_list')

    return render(request, 'adminpanel/hero_banner_update.html', {'banner': banner})

@login_required(login_url='admin_login')
def hero_banner_delete(request, pk):
    item = get_object_or_404(HeroBanner, pk=pk)
    item.delete()
    return redirect('admin_hero_banner_list')


# SeasonalBanner
@login_required(login_url='admin_login')
def seasonal_banner_list(request):
    item = SeasonalBanner.objects.latest('created_at')
    return render(request, 'adminpanel/seasonal_banner_list.html', {'banner': item})

@login_required(login_url='admin_login')
def seasonal_banner_create(request):
    if request.method == 'POST':
        season = request.POST.get('bannerTitle')
        image_desktop = request.FILES.get('bannerImage')

        if season and image_desktop:
            SeasonalBanner.objects.create(season=season, image_desktop=image_desktop)
            return redirect('admin_seasonal_banner_list')
        else:
            error = "All fields are required."
            return render(request, 'adminpanel/seasonal_banner_form.html', {'error': error})
    
    return render(request, 'adminpanel/seasonal_banner_form.html')


@login_required(login_url='admin_login')
def seasonal_banner_update(request, pk):
    item = get_object_or_404(SeasonalBanner, pk=pk)

    if request.method == 'POST':
        season = request.POST.get('bannerTitle')
        image_desktop = request.FILES.get('bannerImage')

        if season:
            item.season = season

        if image_desktop:
            item.image_desktop = image_desktop

        item.save()
        return redirect('admin_seasonal_banner_list')

    return render(request, 'adminpanel/seasonal_banner_update.html', {
        'item': item
    })

@login_required(login_url='admin_login')
def seasonal_banner_delete(request, pk):
    item = get_object_or_404(SeasonalBanner, pk=pk)
    item.delete()
    return redirect('admin_seasonal_banner_list')


@login_required(login_url='admin_login')
def client_review_list(request):
    client_review = ClientReview.objects.all().order_by('-created_at')
    client_review_paginator = Paginator(client_review, 10) 
    client_review_page_number = request.GET.get('contact_page')
    client_reviews = client_review_paginator.get_page(client_review_page_number)

    return render(request, 'adminpanel/client_review_list.html', {
        'client_reviews': client_reviews,
    })


@login_required(login_url='admin_login')
def client_review_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        message = request.POST.get('message')

        if name and message:
            ClientReview.objects.create(
                name=name,
                message=message,
                image=image,
            )
            return redirect('admin_client_review_list')

    return render(request, 'adminpanel/create_client_review.html')

@login_required(login_url='admin_login')
def client_review_update(request, pk):
    review = get_object_or_404(ClientReview, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        image = request.FILES.get('image')

        review.name = name
        review.message = message

        if image:
            review.image = image

        review.save()
        return redirect('admin_client_review_list')

    return render(request, 'adminpanel/update_client_review.html', {'review': review})

@login_required(login_url='admin_login')
def client_review_delete(request, pk):
    item = get_object_or_404(ClientReview, pk=pk)
    item.delete()
    return redirect('admin_client_review_list')
