from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import (
    acheck_password,
    check_password,
    is_password_usable,
    make_password,
)
from shortuuidfield import ShortUUIDField


class UserStatusChoices(models.IntegerChoices):
    ACTIVED = 1
    UNACTIVE = 2
    LOCKED = 3


class OAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):
        """
        创建用户
        """
        if not realname:
            raise ValueError("必须设置真是姓名")
        email = self.normalize_email(email)
        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, realname, email=None, password=None, **extra_fields):
        """
        创建普通用户
        :param username:
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)

    def create_superuser(self, realname, email=None, password=None, **extra_fields):
        """
        创建超级用户
        :param username:
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatusChoices.ACTIVED)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)


# Create your models here.

# 重写User模型
class OAUser(AbstractBaseUser, PermissionsMixin):
    """
     自定义的User模型
    """
    # class Meta:
    #     ordering = ("-date_joined",)
    # username_validator = UnicodeUsernameValidator()
    uid = ShortUUIDField(primary_key=True)
    realname = models.CharField(
        # _("username"),
        max_length=150,
        unique=False,
        # help_text=_(
        #     "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        # ),
        # validators=[username_validator],
        #     error_messages={
        #         "unique": _("A user with that username already exists."),
        #     },
    )
    # first_name = models.CharField(_("first name"), max_length=150, blank=True)
    # last_name = models.CharField(_("last name"), max_length=150, blank=True)
    #

    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(max_length=20, blank=True)
    is_staff = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    status = models.IntegerField(choices=UserStatusChoices.choices, default=UserStatusChoices.UNACTIVE)

    date_joined = models.DateTimeField(auto_now_add=True)

    department = models.ForeignKey('OADepartment', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='staffs',related_query_name='staffs')

    objects = OAUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["realname", "password"]

    # class Meta:
    #     verbose_name = _("user")
    #     verbose_name_plural = _("users")
    #     abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        # full_name = "%s %s" % (self.first_name, self.last_name)
        # return full_name.strip()
        return self.realname

    def get_short_name(self):
        """Return the short name for the user."""
        # return self.first_name
        return self.realname

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

class OADepartment(models.Model):
    name  = models.CharField(max_length=150)
    intro = models.CharField(max_length=150)
    # leader
    leader = models.OneToOneField(OAUser, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="leader_department",related_query_name="leader_department")
    # manager
    manager  = models.ForeignKey(OAUser, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="manager_departments",related_query_name="manager_departments")
