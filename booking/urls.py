from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('search-packages/', views.search_packages, name='search_packages'),
    # ---- INDIA TOURS ROUTES ----
    path('india-tours/<slug:subcategory_slug>/<slug:package_slug>/', views.package_detail_view, name='package_detail'),
    path('india-tours/<slug:subcategory_slug>/', views.india_subcategory_detail, name='india_subcategory_detail'),
    path('india-tours/', views.india_tours_view, name='india_tours'),

    # ---- OTHERS ----
    
    path('international-tours/<slug:subcategory_slug>/<slug:package_slug>/', views.international_package_detail_view, name='international_package_detail'),
    path('international-tours/<slug:subcategory_slug>/', views.international_subcategory_detail, name='international_subcategory_detail'),
    path('international-tours/', views.international_tours_view, name='international_tours'),

    path('ayurveda/', views.ayurveda_tours_view, name='ayurveda_tours'),
    path('ayurveda/<slug:package_slug>/', views.ayurveda_package_detail_view, name='ayurveda_package_detail'),

    path('resort/<int:pk>/', views.resort_detail, name='resort_detail'),
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('submit-review/<int:item_id>/<str:item_type>/', views.submit_review, name='submit_review'),

    
    
]
   


