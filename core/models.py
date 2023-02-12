from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = ('ADMIN', 'Admin')
        LEADER = ('LEADER', 'Leader')
        MEMBER = ('MEMBER', 'Member')
        GUEST = ('GUEST', 'Guest')

    role = models.CharField(
        name='Role',
        max_length=50,
        choices=Role.choices,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Users"


class Usa_State(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        verbose_name_plural = "Usa_States"

    def __str__(self):
        return self.name


class City(models.Model):
    selected_state = models.ForeignKey(
        Usa_State,
        verbose_name="Usa_States",
        on_delete=models.CASCADE
        )
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class Contact(models.Model):
    fullname = models.CharField(max_length=75)
    contact_email = models.EmailField()
    contact_subject = models.CharField(max_length=50)
    contact_message = models.TextField()
    inserted_date = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        verbose_name_plural = "Catalog_Contacts"

    def __str__(self):
        return self.fullname


class Org(models.Model):
    name = models.CharField(max_length=150)
    org_city = models.CharField(max_length=100)
    org_state = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Orgs"

    def __str__(self):
        return self.name + '-' + self.org_city + '-' + org_state


class Ministry(models.Model):
    name = models.CharField(max_length=150)
    org =  models.ForeignKey(
        Org,
        verbose_name="Orgs",
        on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "Ministries"

    def __str__(self):
        return self.name + '_' + self.org


class MinistryRole(models.Model):
    name = models.CharField(max_length=150)
    ministry_department = models.ForeignKey(
        Ministry,
        verbose_name="Ministries",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "MinistryRoles"

    def __str__(self):
        return self.name


class MinistryTeamMember(models.Model):
    team_member = models.ForeignKey(
        User,
        verbose_name="Users",
        on_delete=models.CASCADE)
    ministry_department = models.ForeignKey(
        Ministry,
        verbose_name="Ministries",
        on_delete=models.CASCADE)
    team_role = models.ForeignKey(
        MinistryRole,
        verbose_name="MinistryRoles",
        on_delete=models.CASCADE)