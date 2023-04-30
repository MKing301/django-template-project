from django.contrib import admin
from .models import (
    Profile,
    Usr_State,
    City,
    Contact,
    Org,
    Ministry,
    MinistryRole
    )

admin.site.register(Profile)
admin.site.register(Usr_State)
admin.site.register(City)
admin.site.register(Contact)
admin.site.register(Org)
admin.site.register(Ministry)
admin.site.register(MinistryRole)
