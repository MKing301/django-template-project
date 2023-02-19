from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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
    ministry_department = models.ForeignKey(
        Ministry,
        verbose_name="Ministries",
        default=None,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "MinistryRoles"

    def __str__(self):
        return self.name + ' - ' + self.ministry_department.name


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = ('ADMIN', 'Admin')
        LEADER = ('LEADER', 'Leader')
        MEMBER = ('MEMBER', 'Member')
        GUEST = ('GUEST', 'Guest')

    class Gender(models.TextChoices):
        FEMALE = ('Female', 'Female')
        MALE = ('Male', 'Male')

    class Marital_Status(models.TextChoices):
        MARRIED = ('Married', 'Married')
        SINGLE = ('Single', 'Single')
        DIVORCED = ('Divorced', 'Divorced')
        WIDOWED = ('Widowed', 'Widowed')

    class Tier(models.TextChoices):
        ONE = ('1', '1')
        TWO = ('2', '2')
        THREE = ('3', '3')

    class Board_Member(models.TextChoices):
        YES = ('Yes', 'Yes')
        NO = ('No', 'No')

    gender = models.CharField(
        name='gender',
        max_length=10,
        choices=Gender.choices,
        null=True,
        blank=True
    )

    marital_status = models.CharField(
        name='marital_status',
        max_length=10,
        choices=Marital_Status.choices,
        null=True,
        blank=True
    )

    tier = models.CharField(
        name='tier',
        max_length=10,
        choices=Tier.choices,
        null=True,
        blank=True
    )

    image_file = models.ImageField(
        upload_to="images/",
        height_field=None,
        width_field=None,
        max_length=125,
        default='images/default.jpg'
        )
    street_number = models.IntegerField(blank=True,null=True)
    street_name = models.CharField(max_length=50, blank=True,null=True)
    usr_city = models.ForeignKey(
        City,
        verbose_name="Cities",
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )
    usr_state = models.ForeignKey(
        Usa_State,
        blank=True,
        null=True,
        verbose_name="Usa_States",
        on_delete=models.CASCADE
        )
    postal_code = models.IntegerField(blank=True,null=True)
    birthdate = models.DateField(null=True, blank=True)
    assigned_elder = models.ForeignKey(
        MinistryRole,
        verbose_name="MinistryRoles",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    board_member = models.CharField(
        name='board_member',
        max_length=10,
        choices=Board_Member.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


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
