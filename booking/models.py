from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    
    # Optional: Customize relationships to Group and Permission to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)

# Category for Tour Packages
class Category(models.Model):
    PARENT_CHOICES = [
        ('india', 'India Tours'),
        ('international', 'International Tours'),
        ('ayurveda', 'Ayurveda & Wellness'),
        ('specials', 'Eastora Specials'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.CASCADE
    )
    parent_choice = models.CharField(
        max_length=20,
        choices=PARENT_CHOICES,
        default='india',
        help_text="Top-level grouping for this category."
    )

    banner_image_desktop = models.ImageField(upload_to='category_banners/desktop/', null=True, blank=True)
    banner_image_mobile = models.ImageField(upload_to='category_banners/mobile/', null=True, blank=True)

    card_image = models.ImageField(upload_to='category_banners/cards/',null=True,blank=True,
        help_text="Image to be shown in category cards or grid views."
    )

    short_description = models.CharField(max_length=255, blank=True)
    long_description = models.TextField(blank=True)
    tittle_first = models.CharField(max_length=100, null=True, blank=True)
    tittle_second = models.CharField(max_length=100, null=True, blank=True)
    content_first = models.TextField(blank=True)
    content_second = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.full_path()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Auto-generate slug from name
        super().save(*args, **kwargs)

    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path()} → {self.name}"
        return self.name

    def get_all_packages(self):
        """Return all packages under this category (including subcategories)."""
        categories = [self.id] + list(self.subcategories.values_list("id", flat=True))
        
        # recursively fetch deeper levels
        def collect_children(cat):
            for child in cat.subcategories.all():
                categories.append(child.id)
                collect_children(child)
        collect_children(self)

        return TourPackage.objects.filter(category_id__in=categories)

    def total_package_count(self):
        return self.get_all_packages().count()
    
# Tour Package Model
class TourPackage(models.Model):
    PARENT_CHOICES = [
        ('india', 'India Tours'),
        ('international', 'International Tours'),
        ('ayurveda', 'Ayurveda & Wellness'),
        ('specials', 'Eastora Specials'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=200)
    tags = TaggableManager(blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    itinerary = models.JSONField(blank=True, null=True, help_text="Day-wise itinerary")
    location = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    nights = models.IntegerField(blank=True, null=True)

    image_desktop = models.ImageField(upload_to='packages/desktop/', null=True, blank=True)
    image_mobile = models.ImageField(upload_to='packages/mobile/', null=True, blank=True)
    card_image = models.ImageField(upload_to='packages/cards/', null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='packages')
    is_featured = models.BooleanField(default=False)

    parent_choice = models.CharField(
        max_length=20,
        choices=PARENT_CHOICES,
        default='india',
        help_text="Top-level classification for the tour package"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def title_main(self):
        return self.title.split('–')[0].strip() if '–' in self.title else self.title

    def __str__(self):
        return self.title

    def get_duration(self):
        return f"{self.days} days {self.nights} nights"


# Resort Model
class Resort(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField()
    image = models.ImageField(upload_to='resorts/')

    def __str__(self):
        return self.name

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_type = models.CharField(max_length=10, choices=[('tour', 'Tour'), ('resort', 'Resort')])
    item_id = models.PositiveIntegerField()
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f'{self.booking_type} booking for {self.user.username}'

# Enquiry Model
class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    related_package = models.ForeignKey('TourPackage', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name} for {self.related_package}"
    

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(verbose_name="Email ID")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.full_name} - {self.destination}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, null=True, blank=True, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.package.title if self.package else self.resort.name}"


# Hero Banner Model
class HeroBanner(models.Model):
    ALIGN_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    image_desktop = models.ImageField(upload_to='banners/hero/desktop/', null=True, blank=True)
    image_mobile = models.ImageField(upload_to='banners/hero/mobile/', null=True, blank=True)
    content_alignment = models.CharField(
        max_length=10, choices=ALIGN_CHOICES, default='left'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Seasonal Banner Model
class SeasonalBanner(models.Model):
    season = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_desktop = models.ImageField(upload_to='banners/seasonal/desktop/', null=True, blank=True)
    image_mobile = models.ImageField(upload_to='banners/seasonal/mobile/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.season} Banner"


class ClientReview(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='client_reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client Review"
        verbose_name_plural = "Client Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"
