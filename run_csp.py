import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_timetable.settings")
django.setup()

from csp import generate_timetable

result = generate_timetable()
if result:
    print("✅ Timetable generation completed successfully.")
else:
    print("❌ Timetable generation failed.")
