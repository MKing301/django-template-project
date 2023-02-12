from django.contrib import admin
from .models import (
    User,
    Usa_State,
    City,
    Contact,
    Org,
    Ministry,
    MinistryRole
    )

admin.site.register(User)
admin.site.register(Usa_State)
admin.site.register(City)
admin.site.register(Contact)
admin.site.register(Org)
admin.site.register(Ministry)
admin.site.register(MinistryRole)
