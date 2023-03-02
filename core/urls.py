from django.urls import path
from .views import (
    DashboardView,
    FeesPaymentView,
    SignInView,
    verify_transaction,
    create_default_superuser,
)

urlpatterns = [
    path("", SignInView.as_view(), name="sign-in"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("fees-payment", FeesPaymentView.as_view(), name="fees-payment"),
    path("verify-transaction", verify_transaction, name="verify-transaction"),
    path(
        "create-default-superuser",
        create_default_superuser,
        name="create-default-superuser",
    ),
]
