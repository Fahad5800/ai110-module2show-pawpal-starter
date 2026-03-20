from dataclasses import dataclass, field
from datetime import date, time
from typing import List, Dict, Any, Optional
from enum import Enum


class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)
    tasks: List["Task"] = field(default_factory=list)

    def update_info(self, name: str, species: str, age: int, special_needs: List[str]):
        """Update the pet's profile fields in place."""
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs

    def add_task(self, task: "Task"):
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        """Remove the task with the given id from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks_due_today(self) -> List["Task"]:
        """Return all tasks scheduled to occur today."""
        return [t for t in self.tasks if t.is_due_today()]

    def get_summary(self) -> str:
        """Return a single-line string summarising the pet's key details."""
        needs = ", ".join(self.special_needs) if self.special_needs else "none"
        return (
            f"{self.name} ({self.species}, age {self.age}) | "
            f"special needs: {needs} | tasks: {len(self.tasks)}"
        )


_task_id_counter = iter(range(1, 10_000))


@dataclass
class Task:
    task_type: str
    duration: int          # minutes
    priority: int          # 1 (highest) – 5 (lowest)
    frequency: Frequency
    pet: Pet
    scheduled_time: Optional[time] = None
    completed: bool = False
    id: int = field(default_factory=lambda: next(_task_id_counter))

    def edit_details(self, task_type: str, duration: int, priority: int, frequency: Frequency):
        """Update the task's core attributes in place."""
        self.task_type = task_type
        self.duration = duration
        self.priority = priority
        self.frequency = frequency

    def is_due_on(self, check_date: date) -> bool:
        """Return True if this task should occur on check_date."""
        if self.frequency == Frequency.DAILY:
            return True
        if self.frequency == Frequency.WEEKLY:
            # due every Monday (weekday 0); adjust as needed
            return check_date.weekday() == 0
        if self.frequency == Frequency.MONTHLY:
            return check_date.day == 1
        return False

    def is_due_today(self) -> bool:
        """Return True if this task is due on today's date."""
        return self.is_due_on(date.today())

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def reset(self):
        """Reset the task to incomplete so it can be re-done."""
        self.completed = False

    def get_description(self) -> str:
        """Return a formatted one-line description of the task including status and schedule."""
        time_str = self.scheduled_time.strftime("%I:%M %p") if self.scheduled_time else "unscheduled"
        status = "done" if self.completed else "pending"
        return (
            f"[{status}] {self.task_type} for {self.pet.name} | "
            f"{self.duration} min | priority {self.priority} | "
            f"{self.frequency.value} | {time_str}"
        )


class Owner:
    def __init__(self, name: str, available_hours: List[int] = None, preferences: Dict[str, Any] = None):
        self.name = name
        self.available_hours = available_hours if available_hours is not None else []
        self.preferences = preferences if preferences is not None else {}
        self.pets: List[Pet] = []

    # --- pet management ---

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove the pet with the given name from this owner's pet list."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return the Pet with the given name, or None if not found."""
        for p in self.pets:
            if p.name == pet_name:
                return p
        return None

    # --- task access across all pets ---

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_all_tasks_due_today(self) -> List[Task]:
        """Return a flat list of today's due tasks across all pets."""
        return [task for pet in self.pets for task in pet.get_tasks_due_today()]

    # --- availability & preferences ---

    def set_availability(self, hours: List[int]):
        """Replace the owner's available hours with the provided list."""
        self.available_hours = hours

    def update_preferences(self, prefs: Dict[str, Any]):
        """Merge the given preferences into the owner's existing preferences dict."""
        self.preferences.update(prefs)

    def get_constraints(self) -> Dict[str, Any]:
        """Return the owner's scheduling constraints (available hours and preferences)."""
        return {
            "available_hours": self.available_hours,
            "preferences": self.preferences,
        }


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.daily_plan: List[Dict[str, Any]] = []

    # --- task routing (delegates to the correct pet) ---

    def add_task(self, task: Task):
        """Add a task directly to its pet's task list."""
        task.pet.add_task(task)

    def remove_task(self, task_id: int):
        """Remove a task by id from whichever pet owns it."""
        for pet in self.owner.pets:
            pet.remove_task(task_id)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find and return a task by its id, or None if not found."""
        for task in self.owner.get_all_tasks():
            if task.id == task_id:
                return task
        return None

    # --- plan generation ---

    def generate_plan(self, for_date: date):
        """
        Build daily_plan for for_date:
        1. Collect all tasks due on that date across every pet.
        2. Sort by priority (1 = highest), then by pet name for stable ordering.
        3. Slot each task into the owner's next free available hour.
        """
        due_tasks = [
            task
            for pet in self.owner.pets
            for task in pet.tasks
            if task.is_due_on(for_date)
        ]
        due_tasks.sort(key=lambda t: (t.priority, t.pet.name))

        constraints = self.owner.get_constraints()
        free_hours = list(constraints.get("available_hours", []))

        self.daily_plan = []
        for task in due_tasks:
            slot = free_hours.pop(0) if free_hours else None
            task.scheduled_time = time(slot) if slot is not None else None
            self.daily_plan.append({
                "task_id": task.id,
                "pet": task.pet.name,
                "task_type": task.task_type,
                "priority": task.priority,
                "duration": task.duration,
                "scheduled_hour": slot,
                "completed": task.completed,
            })

    def mark_task_complete(self, task_id: int):
        """Mark a task complete by id and sync the daily plan entry."""
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_complete()
            for entry in self.daily_plan:
                if entry["task_id"] == task_id:
                    entry["completed"] = True

    # --- reporting ---

    def get_tasks_by_pet(self) -> Dict[str, List[Task]]:
        """Return all tasks grouped by pet name."""
        return {pet.name: pet.tasks for pet in self.owner.pets}

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across every pet."""
        return [t for t in self.owner.get_all_tasks() if not t.completed]

    def get_plan_summary(self) -> str:
        """Return a human-readable multi-line summary of the current daily plan."""
        if not self.daily_plan:
            return "No plan generated yet."
        lines = [f"Daily plan ({len(self.daily_plan)} tasks):"]
        for entry in self.daily_plan:
            hour = f"{entry['scheduled_hour']:02d}:00" if entry["scheduled_hour"] is not None else "unscheduled"
            status = "done" if entry["completed"] else "pending"
            lines.append(
                f"  {hour} | [{status}] {entry['task_type']} for {entry['pet']} "
                f"({entry['duration']} min, priority {entry['priority']})"
            )
        return "\n".join(lines)
