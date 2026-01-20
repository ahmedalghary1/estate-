from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Property(models.Model):
    """
    Property model with multilingual support (English and Arabic)
    """
    PROPERTY_TYPE_CHOICES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Land', 'Land'),
        ('Office', 'Office'),
    ]
    
    SALE_TYPE_CHOICES = [
        ('Sale', 'For Sale'),
        ('Rent', 'For Rent'),
    ]
    
    # Owner information
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    
    # Multilingual fields
    title_en = models.CharField(max_length=200, verbose_name='Title (English)')
    title_ar = models.CharField(max_length=200, verbose_name='Title (Arabic)')
    description_en = models.TextField(verbose_name='Description (English)')
    description_ar = models.TextField(verbose_name='Description (Arabic)')
    location_en = models.CharField(max_length=200, verbose_name='Location (English)')
    location_ar = models.CharField(max_length=200, verbose_name='Location (Arabic)')
    
    # Property details
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    
    # Status and timestamps
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title_en} - {self.property_type}"
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
    
    def get_title(self, language='en'):
        """Get title in specified language"""
        return self.title_ar if language == 'ar' else self.title_en
    
    def get_description(self, language='en'):
        """Get description in specified language"""
        return self.description_ar if language == 'ar' else self.description_en
    
    def get_location(self, language='en'):
        """Get location in specified language"""
        return self.location_ar if language == 'ar' else self.location_en


class PropertyImage(models.Model):
    """
    Property images with ordering support
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/%Y/%m/%d/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.property.title_en}"
    
    class Meta:
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'
        ordering = ['order', '-created_at']
