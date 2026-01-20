from django.urls import path
from .views import SignupView, MedicineListView, MedicineCreateView, MedicineUpdateView, MedicineDeleteView, mark_medicine_taken, MedicineAnalyticsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', MedicineListView.as_view(), name='medicine_list'),
    path('analytics/', MedicineAnalyticsView.as_view(), name='medicine_analytics'),
    path('add/', MedicineCreateView.as_view(), name='medicine_add'),
    path('<int:pk>/edit/', MedicineUpdateView.as_view(), name='medicine_edit'),
    path('<int:pk>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),
    path('<int:pk>/taken/', mark_medicine_taken, name='medicine_mark_taken'),
]
