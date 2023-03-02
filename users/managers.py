from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    `UserManager` where matriculation number is the unique identifier for
    authentication instead of usernames.
    """

    def create_student(self, identifier: str, password: str, **extra_fields):
        """
        Creates and saves a student with the given matriculation number and password.
        """
        if not identifier:
            raise ValueError(_("Identifier must be set"))
        student = self.model(identifier=identifier, **extra_fields)
        student.set_password(password)
        student.save()
        return student

    def create_superuser(self, identifier: str, password: str, **extra_fields):
        """
        Creates a super user with the given `admin_id` and `password`.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have `is_staff=True`"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have `is_superuser=True`"))
        return self.create_student(identifier, password, **extra_fields)
