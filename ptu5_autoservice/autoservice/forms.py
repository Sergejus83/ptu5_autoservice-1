from django import forms
from . models import OrderReview

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('comments', 'user', 'order')
        widgets = {
            'user': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }


