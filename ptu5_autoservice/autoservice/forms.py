from django import forms
from . models import OrderReview, Order

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('comments', 'user', 'order')
        widgets = {
            'user': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('order', 'due_back', )
#         # widgets = {'due_back': DateInput()}
