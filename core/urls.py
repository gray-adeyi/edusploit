from django.urls import path
from .views import DashboardView, FeesPaymentView, SignInView

urlpatterns = [
    path("", SignInView.as_view(), name="sign-in"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("fees-payment", FeesPaymentView.as_view(), name="fees-payment"),
]
