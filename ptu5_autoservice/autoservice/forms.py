from django import forms
# from django.utils.timezone import datetime, timedelta
from . models import OrderReview, Order


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('comments', 'user', 'order')
        widgets = {
            'user': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('car', 'estimate_date',)
        widgets = {'estimate_date': DateInput()}


class BookInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('car', 'estimate_date', )
        widgets = {'estimate_date': DateInput(), 'car': forms.HiddenInput()}