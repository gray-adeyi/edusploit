from django.views.generic import TemplateView


class SignInView(TemplateView):
    template_name = "core/sign-in.html"


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"


class FeesPaymentView(TemplateView):
    template_name = "core/fees-payment.html"
