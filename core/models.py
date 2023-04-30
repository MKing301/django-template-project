import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Usr_State(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        verbose_name_plural = "Usr_States"

    def __str__(self):
        return self.name


class City(models.Model):
    selected_state = models.ForeignKey(
        Usr_State,
        verbose_name="Usr_States",
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
        Usr_State,
        verbose_name="Usr_States",
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


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

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
        Usr_State,
        blank=True,
        null=True,
        verbose_name="Usr_States",
        on_delete=models.CASCADE
        )
    postal_code = models.IntegerField(blank=True,null=True)
    image = models.ImageField(
        upload_to="profile_pic",
        default='default.png'
        )


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    # Override the save method of the model
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path) # Open image
        print(self.image.path)

        # resize image
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image


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
