from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from typing import Any
from .models import Billable, Transaction
from users.models import User


class SignInView(TemplateView):
    template_name = "core/sign-in.html"

    def post(self, request):
        identifier = request.POST["identifier"]
        password = request.POST["password"]
        user = authenticate(request, identifier=identifier, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return redirect("sign-in")


class BaseView(LoginRequiredMixin, TemplateView):
    ...


class DashboardView(BaseView):
    template_name = "core/dashboard.html"


class FeesPaymentView(BaseView):
    template_name = "core/fees-payment.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["PAYSTACK_PUBLIC_KEY"] = settings.PAYSTACK_PUBLIC_KEY
        return context


@csrf_exempt
def verify_transaction(request):
    if request.method == "POST":
        billable = get_object_or_404(
            Billable, user=request.user, id=request.POST["billable_id"]
        )
        transaction = Transaction.objects.create(
            billable=billable, ref_id=request.POST["ref_id"]
        )
        transaction_status = transaction.verify()
        return JsonResponse(data={"transaction_status": transaction_status})
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


# RENDER does not support shells for their free tiers
# so this a bad hack to create a default super user so the
# admin can be accessed
def create_default_superuser(request):
    try:
        User.objects.get(identifier=settings.DEFAULT_ADMIN_IDENTIFIER)
        return HttpResponse("<h1>Admin already exist</h1>")
    except User.DoesNotExist:
        User.objects.create_superuser(
            identifier=settings.DEFAULT_ADMIN_IDENTIFIER,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
        return HttpResponse("<h1>Admin successfully created</h1>")
