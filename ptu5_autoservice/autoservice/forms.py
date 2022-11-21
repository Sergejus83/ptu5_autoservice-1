from django import forms
from . models import OrderRevew

class OrderReviewForm(forms.ModelForm):
      class Meta:
        model = OrderRevew
        fields = ('comments', 'user', 'order')
        widgets = {
            'user': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }


