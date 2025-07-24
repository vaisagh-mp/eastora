from django import forms
from .models import (
    Category, TourPackage, Booking, HeroBanner, SeasonalBanner,
    Resort, Enquiry, Contact, Review
)

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'contact_number']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'destination', 'contact_number', 'email', 'message']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class HeroBannerForm(forms.ModelForm):
    class Meta:
        model = HeroBanner
        fields = '__all__'

class SeasonalBannerForm(forms.ModelForm):
    class Meta:
        model = SeasonalBanner
        fields = '__all__'
