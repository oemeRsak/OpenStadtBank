from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("modern/", views.modern_dashboard, name="modern-dashboard"),
    path("modern/customers/", views.modern_customers, name="modern-customers"),
    path("modern/credit/", views.modern_credit, name="modern-credit"),
    path("modern/login/", views.modern_login, name="modern-login"),
    path("modern/payment/", views.modern_payment, name="modern-payment"),
    path("modern/settings/", views.modern_settings, name="modern-settings"),
]