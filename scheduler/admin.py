from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Supervisor, Agent, Judge, RecurringCourtSlot, SpecialtyAssignment, MonthlyAssignment, TimeOffRequest

# Register the custom user model (Supervisor)
@admin.register(Supervisor)
class SupervisorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

# Register the other models simply
admin.site.register(Agent)
admin.site.register(Judge)
admin.site.register(RecurringCourtSlot)
admin.site.register(SpecialtyAssignment)
admin.site.register(MonthlyAssignment)
admin.site.register(TimeOffRequest)