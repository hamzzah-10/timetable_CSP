from django.shortcuts import render
from django.http import HttpResponse
from timetable.csp import generate_timetable

# Create your views here.
def home (request):
    return HttpResponse('Test')

def generate_timetable_view(request):
    success = generate_timetable()
    if success:
        return HttpResponse("Timetable generated successfully!")
    else:
        return HttpResponse("Failed to generate timetable. Check the logs for details.")

