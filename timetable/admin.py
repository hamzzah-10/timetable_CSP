from django.contrib import admin
from .models import ClassRoom, Teacher, Subject, TimeSlot, Room, TimetableEntry
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
import subprocess
import os
from timetable.models import *
from timetable.csp import generate_timetable  # <-- import properly

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    # change_list_template = "admin/changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-timetable/', self.admin_site.admin_view(self.generate_timetable), name="generate-timetable")
        ]
        return custom_urls + urls

    def generate_timetable(self, request):
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            generate_timetable()
            self.message_user(request, "✅ Timetable generated successfully.", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"❌ Failed: {str(e)}", level=messages.ERROR)
        return HttpResponseRedirect("../")

# Register other models normally
admin.site.register(ClassRoom)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(TimeSlot)
admin.site.register(Room)
