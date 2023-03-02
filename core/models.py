from django.db import models
from users.models import Session, Level, User
from decimal import Decimal
from django.conf import settings
from pypaystack2 import Paystack


class TransactionStatus(models.TextChoices):
    PENDING = "pending"
    FAILED = "failed"
    SUCCESSFUL = "successful"


class Billing(models.Model):
    fees_name = models.CharField(max_length=200)
    fees_description = models.TextField()
    session = models.CharField(max_length=10, choices=Session.choices)
    level = models.CharField(max_length=15, choices=Level.choices)
    due_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return self.fees_name


class Billable(models.Model):
    billing = models.OneToOneField(Billing, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="billables"
    )

    def total_outstanding(self) -> Decimal:
        return self.billing.total_amount - self.total_paid_fees()

    def has_complete_payment(self) -> bool:
        return self.billing.total_amount == self.total_paid_fees()

    def total_paid_fees(self) -> Decimal:
        total = Decimal("0")
        for transaction in self.transactions.all():
            if transaction.status == TransactionStatus.SUCCESSFUL:
                total += transaction.total_paid_fees
        return total

    def __str__(self) -> str:
        return f"{self.billing} for {self.user}"


class Transaction(models.Model):
    billable = models.ForeignKey(
        Billable, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    ref_id = models.CharField(max_length=15)
    total_paid_fees = models.DecimalField(
        max_digits=9, decimal_places=2, default=Decimal("0")
    )
    status = models.CharField(
        max_length=15,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    def verify(self) -> TransactionStatus:
        paystack = Paystack(auth_key=settings.PAYSTACK_SECRET_KEY)
        response = paystack.transactions.verify(self.ref_id)
        if response.status_code == 200 and response.status is True:
            self.total_paid_fees = Decimal(response.data["amount"] / 100)
            self.status = TransactionStatus.SUCCESSFUL
            self.save()
            return self.status
        else:
            self.status = TransactionStatus.FAILED
            self.save()
            return self.status

    def __str__(self) -> str:
        return self.ref_id
