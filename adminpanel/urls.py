from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='admin_login'),
    path('logout/', views.logout_view, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('toggle-featured/', views.toggle_featured_status, name='toggle_featured_status'),
    path('toggle-featured-active/', views.toggle_featured_is_active, name='toggle_featured_is_active'),
    path('category/<int:pk>/toggle-featured/', views.toggle_featured, name="toggle_featured"),


    path('categories/', views.category_list, name='admin_category_list'),
    path('categories/add/', views.category_create, name='admin_category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='admin_category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='admin_category_delete'),

    path('tourpackages/', views.tourpackage_list, name='admin_tourpackage_list'),
    path('tourpackages/add/', views.tourpackage_create, name='admin_tourpackage_create'),
    path('tourpackages/<int:pk>/edit/', views.tourpackage_update, name='admin_tourpackage_update'),
    path('tourpackages/<int:pk>/delete/', views.tourpackage_delete, name='admin_tourpackage_delete'),

    path('bookings/', views.booking_list, name='admin_booking_list'),
    path('bookings/add/', views.booking_create, name='admin_booking_create'),
    path('bookings/<int:pk>/edit/', views.booking_update, name='admin_booking_update'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='admin_booking_delete'),

    path('enquiries/', views.enquiry_list, name='admin_enquiry_list'),
    path('enquiries/<int:pk>/', views.enquiry_detail, name='enquiry_detail'),
    path('contact-enquiries/<int:pk>/', views.contact_enquiry_detail, name='contact_enquiry_detail'),
    path('enquiries/add/', views.enquiry_create, name='admin_enquiry_create'),
    path('enquiries/<int:pk>/edit/', views.enquiry_update, name='admin_enquiry_update'),
    path('enquiries/<int:pk>/delete/', views.enquiry_delete, name='admin_enquiry_delete'),

    path('contacts/', views.contact_list, name='admin_contact_list'),
    path('contacts/add/', views.contact_create, name='admin_contact_create'),
    path('contacts/<int:pk>/edit/', views.contact_update, name='admin_contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='admin_contact_delete'),

    path('hero-banners/', views.hero_banner_list, name='admin_hero_banner_list'),
    path('hero-banners/add/', views.hero_banner_create, name='admin_hero_banner_create'),
    path('hero-banners/<int:pk>/edit/', views.hero_banner_update, name='admin_hero_banner_update'),
    path('hero-banners/<int:pk>/delete/', views.hero_banner_delete, name='admin_hero_banner_delete'),

    path('seasonal-banners/', views.seasonal_banner_list, name='admin_seasonal_banner_list'),
    path('seasonal-banners/add/', views.seasonal_banner_create, name='admin_seasonal_banner_create'),
    path('seasonal-banners/<int:pk>/edit/', views.seasonal_banner_update, name='admin_seasonal_banner_update'),
    path('seasonal-banners/<int:pk>/delete/', views.seasonal_banner_delete, name='admin_seasonal_banner_delete'),


    path('client-review/', views.client_review_list, name='admin_client_review_list'),
    path('client-review/add/', views.client_review_create, name='admin_client_review_create'),
    path('client-review/<int:pk>/edit/', views.client_review_update, name='admin_client_review_update'),
    path('client-review/<int:pk>/delete/', views.client_review_delete, name='admin_client_review_delete'),




]
