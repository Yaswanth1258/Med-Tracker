from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from .models import Medicine, MedicineLog
from .forms import MedicineForm, UserSignupForm

class SignupView(CreateView):
    form_class = UserSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class MedicineListView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = 'medicines/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        
        # Fetch status for each medicine for today
        medicines = context['medicines']
        for medicine in medicines:
            # Check if there is a log for today
            log = MedicineLog.objects.filter(medicine=medicine, date=today).first()
            medicine.is_taken_today = log.taken if log else False
            
        # Analytics Data: Last 7 Days
        last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        dates = [d.strftime('%a') for d in last_7_days] # ['Mon', 'Tue', ...]
        counts = []
        
        for d in last_7_days:
            # Count how many logs exist with taken=True for this user on this date
            count = MedicineLog.objects.filter(
                medicine__user=self.request.user, 
                date=d, 
                taken=True
            ).count()
            counts.append(count)
            
        context['chart_dates'] = dates
        context['chart_counts'] = counts
        return context

    def get_queryset(self):
        # Only show medicines belonging to the current user
        return Medicine.objects.filter(user=self.request.user).order_by('frequency_amount', '-created_at')

class MedicineAnalyticsView(LoginRequiredMixin, ListView):
    model = MedicineLog
    template_name = 'medicines/analytics.html'
    context_object_name = 'logs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        
        # Analytics Data: Last 7 Days
        last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        dates = [d.strftime('%a') for d in last_7_days] # ['Mon', 'Tue', ...]
        counts = []
        
        for d in last_7_days:
            # Count how many logs exist with taken=True for this user on this date
            count = MedicineLog.objects.filter(
                medicine__user=self.request.user, 
                date=d, 
                taken=True
            ).count()
            counts.append(count)
            
        context['chart_dates'] = dates
        context['chart_counts'] = counts
        return context

    def get_queryset(self):
        return MedicineLog.objects.filter(medicine__user=self.request.user)

def mark_medicine_taken(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    today = timezone.localdate()
    
    # Create or update log
    log, created = MedicineLog.objects.get_or_create(medicine=medicine, date=today)
    log.taken = not log.taken # Toggle status
    log.taken_at = timezone.now() if log.taken else None
    log.save()
    
    return redirect('medicine_list')

class MedicineCreateView(LoginRequiredMixin, CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicines/medicine_form.html'
    success_url = reverse_lazy('medicine_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MedicineUpdateView(LoginRequiredMixin, UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicines/medicine_form.html'
    success_url = reverse_lazy('medicine_list')

    def get_queryset(self):
        # Ensure users can only edit their own medicines
        return Medicine.objects.filter(user=self.request.user)

class MedicineDeleteView(LoginRequiredMixin, DeleteView):
    model = Medicine
    template_name = 'medicines/medicine_confirm_delete.html'
    success_url = reverse_lazy('medicine_list')

    def get_queryset(self):
        # Ensure users can only delete their own medicines
        return Medicine.objects.filter(user=self.request.user)
