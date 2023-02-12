from django.contrib import admin
from .models import (
    User,
    UserDetail,
    Usa_State,
    City,
    Contact,
    Org,
    Ministry,
    MinistryRole,
    MinistryTeamMember
    )


admin.site.register(User)
admin.site.register(UserDetail)
admin.site.register(Usa_State)
admin.site.register(City)
admin.site.register(Contact)
admin.site.register(Org)
admin.site.register(Ministry)
admin.site.register(MinistryRole)
admin.site.register(MinistryTeamMember)
