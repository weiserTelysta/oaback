# Generated by Django 5.1.2 on 2024-10-30 19:16

import apps.oaauth.models
import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="OAUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "uid",
                    shortuuidfield.fields.ShortUUIDField(
                        blank=True,
                        editable=False,
                        max_length=22,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("realname", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("telephone", models.CharField(blank=True, max_length=20)),
                ("is_staff", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Actived"), (2, "Unactive"), (3, "Locked")],
                        default=2,
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", apps.oaauth.models.OAUserManager()),
            ],
        ),
    ]