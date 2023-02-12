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

    def __str__(self):
        return self.first_name + ' ' + self.last_name


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

    class Meta:
        verbose_name_plural = "Cities"

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
    org_city = models.ForeignKey(
        City,
        verbose_name="Cities",
        on_delete=models.CASCADE
        )
    org_state = models.ForeignKey(
        Usa_State,
        verbose_name="Usa_States",
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name_plural = "Orgs"

    def __str__(self):
        return self.name + '-' + self.org_city.name + '-' + self.org_state.name


class Ministry(models.Model):
    name = models.CharField(max_length=150)
    org = models.ForeignKey(
        Org,
        verbose_name="Orgs",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Ministries"

    def __str__(self):
        return self.name + '_' + self.org.name


class MinistryRole(models.Model):
    name = models.CharField(max_length=150)

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

    class Meta:
        verbose_name_plural = "MinistryTeamMembers"

    def __str__(self):
        return self.team_member.first_name + ' ' + self.team_member.last_name + ' ' + self.team_role.name + ' ' + self.ministry_department.name


class UserDetail(models.Model):
    class Gender(models.TextChoices):
        FEMALE = ('FEMALE', 'Female')
        MALE = ('MALE', 'Male')

    class Marital_Status(models.TextChoices):
        MARRIED = ('MARRIED', 'Married')
        SINGLE = ('SINGLE', 'Single')
        DIVORCED = ('DIVORCED', 'Divorces')
        WIDOWED = ('WIDOWED', 'Widowed')

    class Tier(models.TextChoices):
        ONE = ('ONE', '1')
        TWO = ('TWO', '2')
        THREE = ('THREE', '3')

    gender = models.CharField(
        name='Gender',
        max_length=10,
        choices=Gender.choices,
        null=True,
        blank=True
    )

    marital_status = models.CharField(
        name='Marital Status',
        max_length=10,
        choices=Marital_Status.choices,
        null=True,
        blank=True
    )

    tier = models.CharField(
        name='Tier',
        max_length=10,
        choices=Tier.choices,
        null=True,
        blank=True
    )

    usr = models.ForeignKey(
        User,
        verbose_name="Users",
        on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=False, default='default.jpg')
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=50)
    usr_city = models.ForeignKey(
        City,
        verbose_name="Cities",
        on_delete=models.CASCADE
        )
    usr_state = models.ForeignKey(
        Usa_State,
        verbose_name="Usa_States",
        on_delete=models.CASCADE
        )
    postal_code = models.IntegerField()
    birthdate = models.DateField(null=True, blank=True)
    assigned_elder = models.ForeignKey(
        MinistryTeamMember,
        verbose_name="MinistryTeamMembers",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    board_member = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "UserDetails"

    def __str__(self):
        return self.usr.first_name + ' ' + self.usr.last_name
