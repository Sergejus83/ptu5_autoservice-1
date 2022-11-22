from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from . forms import OrderReviewForm, OrderForm
from . import models


def index(request):
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1  
    return render(request, 'autoservice/index.html', {
        'cars_count': models.Car.objects.count(),
        'services_count': models.Service.objects.count(),
        'orders_count': models.Order.objects.count(),
        'visits_count': visits_count,
    })

def car_list_view(request):
    car_list = models.Car.objects.all()
    search = request.GET.get('search')
    if search:
        car_list = car_list.filter(
            Q(client__icontains=search) |
            Q(plate__icontains=search) |
            Q(car_model__make__icontains=search) |
            Q(car_model__model__icontains=search)
        )
    paginator = Paginator(car_list, 2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, 'autoservice/car_list.html', {
        'car_list': paged_cars,
    })

def car_detail_view(request, pk):
    return render(request, 'autoservice/car_detail.html', {
        'object': get_object_or_404(models.Car, pk=pk),
    })


class OrderListView(ListView):
    model = models.Order
    paginate_by = 2
    template_name = 'autoservice/order_list.html'

    def get_queryset(self):
        queryset =  super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            try:
                queryset = queryset.filter(id__exact=search)
            except ValueError:
                queryset = queryset.filter(
                    Q(car__client__icontains=search) |
                    Q(car__plate__icontains=search)
                )
        return queryset


class OrderDetailView(FormMixin, generic.DetailView):
    model = models.Order
    form_class = OrderReviewForm
    template_name = 'autoservice/order_detail.html'

    def get_success_url(self): # kur nukeliaus komentaras
        return reverse('order', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.objects = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(self.request, "you posted too much")
            return self.form_invalid(form)

    def form_valid(self, form):
            form.instance.order = self.get_object()
            form.instance.user = self.request.user
            form.save()
            messages.success(self.request, 'Your review has been posted')
            return super().form_valid(form)

    def get_initial(self):
        return {
            'order': self.get_object(),
            'user': self.request.user
        }


class UserOrderListView(LoginRequiredMixin, ListView):
    model = models.Order
    template_name = 'autoservice/user_order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-estimate_date')
        return queryset


class UserOrderCreateView(LoginRequiredMixin, CreateView):
    model = models.Order
    # fields = ('car', 'estimate_date',)
    form_class = OrderForm
    template_name = 'autoservice/user_order_create.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'n'
        messages.success(self.request, 'new order was added')
        return super().form_valid(form)


class UserOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Order
    # fields = ('car', 'estimate_date',)
    form_class = OrderForm
    template_name = 'autoservice/user_order_update.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'p'
        messages.success(self.request, 'Order was paid')
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user

    
class UserOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Order
    template_name = 'autoservice/user_order_delete.html'
    success_url = reverse_lazy('user_orders')

    def test_func(self):
        order = self.get_object()
        # messages.success(self.request, 'order canselled')
        return self.request.user == order.user

    def form_valid(self, form):
        order = self.get_object()
        if order.status == 'n':
            messages.success(self.request, 'order cancelled')
        # else:
        #     messages.success(self.request, 'please pay')
        return super().form_valid(form)
