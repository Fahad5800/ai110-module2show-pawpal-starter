import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task, Frequency


def make_pet():
    return Pet(name="Buddy", species="Dog", age=3)


def make_task(pet):
    return Task(
        task_type="Morning Walk",
        duration=30,
        priority=1,
        frequency=Frequency.DAILY,
        pet=pet,
    )


def test_mark_complete_changes_status():
    pet = make_pet()
    task = make_task(pet)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = make_pet()
    assert len(pet.tasks) == 0

    task = make_task(pet)
    pet.add_task(task)
    assert len(pet.tasks) == 1

    pet.add_task(make_task(pet))
    assert len(pet.tasks) == 2


if __name__ == "__main__":
    test_mark_complete_changes_status()
    print("PASS  test_mark_complete_changes_status")

    test_add_task_increases_pet_task_count()
    print("PASS  test_add_task_increases_pet_task_count")
