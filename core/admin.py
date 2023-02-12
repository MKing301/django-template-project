from django.contrib import admin
from .models import User, Contact, Org, Ministry, MinistryRole, MinistryTeamMember


admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Org)
admin.site.register(Ministry)
admin.site.register(MinistryRole)
admin.site.register(MinistryTeamMember)

