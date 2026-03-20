from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)

    def update_info(self, name: str, species: str, age: int, special_needs: List[str]):
        pass

    def get_summary(self) -> str:
        pass


@dataclass
class Task:
    task_type: str
    duration: int
    priority: int
    frequency: str
    pet: Pet

    def edit_details(self, task_type: str, duration: int, priority: int, frequency: str):
        pass

    def is_due_today(self) -> bool:
        pass

    def get_description(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_hours: List[int] = None, preferences: Dict[str, Any] = None):
        self.name = name
        self.available_hours = available_hours if available_hours is not None else []
        self.preferences = preferences if preferences is not None else {}

    def set_availability(self, hours: List[int]):
        pass

    def update_preferences(self, prefs: Dict[str, Any]):
        pass

    def get_constraints(self) -> Dict[str, Any]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task] = None):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks if tasks is not None else []
        self.daily_plan: List[Dict[str, Any]] = []

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_id: int):
        pass

    def generate_plan(self, date: Any):
        pass

    def get_plan_summary(self) -> str:
        pass
