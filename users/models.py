from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager
from decimal import Decimal


class UserTypes(models.TextChoices):
    SUPER_USER = "super_user"
    LECTURER = "lecturer"
    STUDENT = "student"


class Level(models.TextChoices):
    L1 = "100 LEVEL"
    L2 = "200 LEVEL"
    L3 = "300 LEVEL"
    L4 = "400 LEVEL"
    L5 = "500 LEVEL"


class Semester(models.TextChoices):
    FIRST = "FIRST SEMESTER"
    SECOND = "SECOND SEMESTER"


class Session(models.TextChoices):
    S2021 = "2021/2022"
    S2022 = "2022/2023"


class EntryMode(models.TextChoices):
    UTME = "UTME"
    DIRECT_ENTRY = "DIRECT_ENTRY"


# TODO: customize the model to meet the needs of different
# user types for now it will have more fields required by
# a student
class User(AbstractBaseUser, PermissionsMixin):
    identifier = models.CharField(max_length=10, unique=True)
    last_name = models.CharField(max_length=15)
    first_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15)
    type = models.CharField(max_length=10, choices=UserTypes.choices)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.identifier


class StudentAdditionalInformation(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="additional_info"
    )
    reg_no = models.CharField(max_length=10)
    email = models.EmailField()
    school_email = models.EmailField()
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    level = models.CharField(max_length=15, choices=Level.choices)
    session = models.CharField(max_length=10, choices=Session.choices)
    semester = models.CharField(max_length=20, choices=Semester.choices)
    entry_mode = models.CharField(max_length=20, choices=EntryMode.choices)
    entry_year = models.CharField(max_length=4)

    def total_bill(self) -> Decimal:
        total = Decimal("0")
        for billable in self.user.billables.all():
            if (
                billable.billing.level == self.level
                and billable.billing.session == self.session
            ):
                total += billable.billing.total_amount
        return total

    def total_payment(self) -> Decimal:
        total = Decimal("0")
        for billable in self.user.billables.all():
            if (
                billable.billing.level == self.level
                and billable.billing.session == self.session
            ):
                total += billable.total_paid_fees()
        return total

    def total_outstanding(self) -> Decimal:
        total = Decimal("0")
        for billable in self.user.billables.all():
            if (
                billable.billing.level == self.level
                and billable.billing.session == self.session
            ):
                total += billable.total_outstanding()
        return total

    def __str__(self) -> str:
        return f"{self.user}"
