from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Property, PropertyImage
from .forms import PropertyForm, PropertyImageFormSet

def property_list(request):
    """
    List all active properties with filtering and pagination
    """
    # Optimized query with prefetch_related
    properties = Property.objects.filter(
        is_active=True
    ).select_related('owner').prefetch_related('images').order_by('-created_at')
    
    # Language selection (from session or default to 'en')
    language = request.session.get('lang', 'en')
    
    # Filtering
    property_type = request.GET.get('type')
    sale_type = request.GET.get('sale_type')
    location = request.GET.get('location')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if property_type:
        properties = properties.filter(property_type=property_type)
    if sale_type:
        properties = properties.filter(sale_type=sale_type)
    if location:
        properties = properties.filter(
            Q(location_en__icontains=location) | Q(location_ar__icontains=location)
        )
    if search:
        properties = properties.filter(
            Q(title_en__icontains=search) | 
            Q(title_ar__icontains=search) |
            Q(description_en__icontains=search) | 
            Q(description_ar__icontains=search)
        )
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(properties, 12)  # Show 12 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique locations for filter dropdown
    locations_en = Property.objects.values_list('location_en', flat=True).distinct()
    locations_ar = Property.objects.values_list('location_ar', flat=True).distinct()
    
    context = {
        'properties': page_obj,
        'page_obj': page_obj,
        'language': language,
        'locations': set(list(locations_en) + list(locations_ar)),
        'property_types': Property.PROPERTY_TYPE_CHOICES,
        'sale_types': Property.SALE_TYPE_CHOICES,
    }
    
    return render(request, 'properties/index.html', context)



def property_detail(request, pk):
    """
    Display detailed view of a single property
    """
    property_obj = get_object_or_404(
        Property.objects.prefetch_related('images'),
        pk=pk,
        is_active=True
    )
    
    # Increment views counter
    property_obj.views += 1
    property_obj.save(update_fields=['views'])
    
    language = request.session.get('lang', 'en')
    
    context = {
        'property': property_obj,
        'language': language,
    }
    
    return render(request, 'properties/detail.html', context)



@login_required
def property_create(request):
    """
    Create a new property (sellers only)
    """
    # Check if user is a seller
    if request.user.profile.user_type != 'seller':
        messages.error(request, 'Only sellers can add properties.')
        return redirect('property_list')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        formset = PropertyImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            
            # Save images
            formset.instance = property_obj
            formset.save()
            
            messages.success(request, 'Property added successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm()
        formset = PropertyImageFormSet()
    
    return render(request, 'properties/form.html', {
        'form': form,
        'formset': formset,
        'title': 'Add New Property'
    })


@login_required
def property_update(request, pk):
    """
    Update an existing property (owner only)
    """
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
        formset = PropertyImageFormSet(instance=property_obj)
    
    return render(request, 'properties/form.html', {
        'form': form,
        'formset': formset,
        'title': 'Edit Property',
        'property': property_obj
    })


@login_required
def property_delete(request, pk):
    """
    Delete a property (owner only)
    """
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('property_list')
    
    return render(request, 'properties/delete_confirm.html', {'property': property_obj})


def set_language(request):
    """
    Switch language (en/ar)
    """
    lang = request.GET.get('lang', 'en')
    request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))
