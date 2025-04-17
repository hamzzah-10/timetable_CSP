import os
import sys


def generate_timetable():
    from timetable.models import ClassRoom, Teacher, Subject, TimeSlot, Room, TimetableEntry
    from ortools.sat.python import cp_model

    # Initialize model
    model = cp_model.CpModel()

    # Fetch data
    classes = list(ClassRoom.objects.all())
    teachers = list(Teacher.objects.all())
    subjects = list(Subject.objects.all())
    slots = list(TimeSlot.objects.all())
    rooms = list(Room.objects.all())

    print(f"📊 Loaded: {len(classes)} classes, {len(subjects)} subjects, {len(teachers)} teachers, {len(rooms)} rooms, {len(slots)} slots")

    # Dictionary to store decision variables
    assignments = {}

    # Step 1: Create variables only for valid (teacher, subject) pairs
    for c_idx, class_ in enumerate(classes):
        for s_idx, subject in enumerate(subjects):
            for t_idx, teacher in enumerate(teachers):
                if subject in teacher.subjects.all():
                    for r_idx, room in enumerate(rooms):
                        for slot_idx, slot in enumerate(slots):
                            key = (c_idx, s_idx, t_idx, r_idx, slot_idx)
                            assignments[key] = model.NewBoolVar(f'C{c_idx}_S{s_idx}_T{t_idx}_R{r_idx}_Slot{slot_idx}')

    # Step 2: Each class can have at most 1 subject per time slot
    for c_idx in range(len(classes)):
        for slot_idx in range(len(slots)):
            model.Add(sum(assignments[key] for key in assignments if key[0] == c_idx and key[4] == slot_idx) <= 1)

    # Step 3: Teacher can be in max 2 sessions per time slot (relaxed)
    for t_idx in range(len(teachers)):
        for slot_idx in range(len(slots)):
            model.Add(sum(assignments[key] for key in assignments if key[2] == t_idx and key[4] == slot_idx) <= 2)

    # Step 4: Room used max 2 times per time slot (relaxed)
    for r_idx in range(len(rooms)):
        for slot_idx in range(len(slots)):
            model.Add(sum(assignments[key] for key in assignments if key[3] == r_idx and key[4] == slot_idx) <= 2)

    # Step 5: Limit sessions for a class-subject to MAX_SESSIONS (relaxed to 10)
    MAX_SESSIONS = 10
    for c_idx in range(len(classes)):
        for s_idx in range(len(subjects)):
            model.Add(sum(assignments[key] for key in assignments if key[0] == c_idx and key[1] == s_idx) <= MAX_SESSIONS)

    # Step 6: Maximize the number of valid assignments
    model.Maximize(sum(assignments.values()))

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0  # Increased time for better results

    print("🔍 Solving CSP...")
    status = solver.Solve(model)

    # Step 7: Save results
    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        TimetableEntry.objects.all().delete()
        true_assignments = [key for key, var in assignments.items() if solver.Value(var) == 1]
        
        print(f"✅ Total assignments made: {len(true_assignments)}")

        for key in true_assignments:
            c_idx, s_idx, t_idx, r_idx, slot_idx = key
            TimetableEntry.objects.create(
                classroom=classes[c_idx],
                subject=subjects[s_idx],
                teacher=teachers[t_idx],
                room=rooms[r_idx],
                timeslot=slots[slot_idx]
            )

            print(f"🧠 {subjects[s_idx].name} → {classes[c_idx].name} | 👨‍🏫 {teachers[t_idx].name} | 🏫 {rooms[r_idx].name} | 📅 {slots[slot_idx].day} Period {slots[slot_idx].period}")

        print(f"🗂️ Timetable entries saved: {len(true_assignments)}")
        return True
    else:
        print("❌ No feasible solution found. Please revise constraints or increase time limit.")
        return False

    print("📈 Solver status:", solver.StatusName())

# Call the function
# if __name__ == "__main__":
#     result = generate_timetable()
#     if result:
#         print("Timetable generation completed successfully.")
#     else:
#         print("Timetable generation failed.")