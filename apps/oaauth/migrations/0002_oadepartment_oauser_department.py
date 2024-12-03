# Generated by Django 5.1.2 on 2024-11-04 21:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("oaauth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OADepartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("intro", models.CharField(max_length=150)),
                (
                    "leader",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="leader_department",
                        related_query_name="leader_department",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "manager",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="manager_departments",
                        related_query_name="manager_departments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="oauser",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="staffs",
                related_query_name="staffs",
                to="oaauth.oadepartment",
            ),
        ),
    ]