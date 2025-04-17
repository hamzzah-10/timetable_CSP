from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subjects = models.ManyToManyField(Subject)
    max_classes_per_day = models.IntegerField(default=6)
    preferred_slots = models.JSONField(default=list, blank=True)  # e.g., ['Monday-1', 'Tuesday-3']

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=20)  # e.g., 10-A
    grade = models.IntegerField()
    section = models.CharField(max_length=1)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # Lab, Lecture, etc.

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    day = models.CharField(max_length=10)  # Monday, Tuesday, etc.
    period = models.IntegerField()         # e.g., 1 to 6
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} - Period {self.period}"

class TimetableEntry(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.classroom} - {self.subject} - {self.timeslot}"
