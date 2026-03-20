from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, Frequency

# --- Setup ---
owner = Owner(name="Alex", available_hours=[8, 9, 10, 14, 16])

buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5, special_needs=["indoor only"])

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks ---
scheduler = Scheduler(owner)

scheduler.add_task(Task(
    task_type="Morning Walk",
    duration=30,
    priority=1,
    frequency=Frequency.DAILY,
    pet=buddy,
))

scheduler.add_task(Task(
    task_type="Feed Breakfast",
    duration=10,
    priority=2,
    frequency=Frequency.DAILY,
    pet=buddy,
))

scheduler.add_task(Task(
    task_type="Clean Litter Box",
    duration=15,
    priority=2,
    frequency=Frequency.DAILY,
    pet=whiskers,
))

scheduler.add_task(Task(
    task_type="Vet Checkup",
    duration=60,
    priority=1,
    frequency=Frequency.MONTHLY,
    pet=whiskers,
))

# --- Generate and print today's schedule ---
today = date.today()
scheduler.generate_plan(today)

print("=" * 50)
print(f"  PawPal+ | Today's Schedule ({today})")
print("=" * 50)

print("\nPets:")
for pet in owner.pets:
    print(f"  {pet.get_summary()}")

print()
print(scheduler.get_plan_summary())

print("\nTask details:")
for entry in scheduler.daily_plan:
    task = scheduler.get_task_by_id(entry["task_id"])
    print(f"  {task.get_description()}")

print("=" * 50)
