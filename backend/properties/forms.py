from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    """
    Form for creating/editing properties with multilingual support
    """
    class Meta:
        model = Property
        fields = [
            'title_en', 'title_ar',
            'description_en', 'description_ar',
            'location_en', 'location_ar',
            'price', 'property_type', 'sale_type', 'phone'
        ]
        widgets = {
            'description_en': forms.Textarea(attrs={'rows': 4}),
            'description_ar': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap/custom classes if needed
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PropertyImageForm(forms.ModelForm):
    """
    Form for uploading property images
    """
    class Meta:
        model = PropertyImage
        fields = ['image', 'order']
        widgets = {
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
        }


# Formset for multiple images
PropertyImageFormSet = forms.inlineformset_factory(
    Property,
    PropertyImage,
    form=PropertyImageForm,
    extra=3,  # Allow uploading 3 images at once
    can_delete=True
)
