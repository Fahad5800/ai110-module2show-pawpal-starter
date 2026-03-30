# PawPal+

**PawPal+** is a Streamlit app that helps pet owners stay consistent with daily pet care. Enter your pet's profile, build a task list, and generate an optimized daily schedule — the app handles prioritization, time-slot fitting, conflict detection, and recurring task management automatically.

---

## Features

### Priority-Based Scheduling
When you generate a schedule, PawPal+ sorts all due tasks by **priority level (1 = highest)**, then by **duration (longest first)**, then alphabetically by pet name. Higher-priority tasks are assigned the earliest available time slots so the most important care happens first.

### Chronological Schedule Display
After a plan is generated, tasks are displayed in **ascending time order** using `get_tasks_sorted_by_time()`. Each row shows the assigned start time, task name, pet, duration, and priority label — giving you a clear, readable daily agenda.

### Time-Slot Fitting
The scheduler converts the owner's available hours into minute-level intervals and greedily assigns each task a contiguous block that fits its duration. Tasks that cannot fit into any remaining slot are flagged as unscheduled rather than silently dropped.

### Capacity Conflict Warnings
If there is not enough available time to fit all due tasks, PawPal+ surfaces a **warning banner** listing every task that could not be scheduled, along with its duration and priority, so you know exactly what was left out and why.

### Time-Overlap Conflict Detection
After slotting tasks, `detect_time_conflicts()` scans all scheduled tasks for **overlapping time intervals** using start/end time comparison. Each overlap is logged and shown in a collapsible panel with both task names and the exact conflicting time range.

### Task Filtering
`filter_tasks(pet_name, completed)` lets you query the task list by pet or completion status. The pending-tasks panel uses this to show only incomplete tasks, sorted by priority, with summary metrics for total, high-priority, and due-today counts.

### Recurring Task Auto-Rescheduling
Tasks marked as **daily, weekly, or monthly** automatically reset after completion via `mark_complete_and_reschedule()`. The task's start date advances to the next correct occurrence (tomorrow for daily, same weekday for weekly, same calendar day for monthly), and the completion flag is cleared so the task reappears on its next due date.

### Non-Crashing Conflict Logging
All conflict detection runs through `ConflictLogger`, which records warnings with timestamps and severity levels and logs them to the console — without raising exceptions or interrupting the schedule generation. The app always produces the best schedule it can and reports problems separately.

---

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover:

| Test | What it verifies |
|---|---|
| `test_mark_complete_changes_status` | Completing a task sets `completed = True` |
| `test_add_task_increases_pet_task_count` | `pet.add_task()` grows the task list correctly |
| `test_filter_tasks_by_pet_and_status` | `filter_tasks()` returns the right subset by pet and status |
| `test_generate_plan_conflict_when_insufficient_hours` | Overflow tasks are recorded in `scheduler.conflicts` |
| `test_get_tasks_sorted_by_time` | Higher-priority tasks receive earlier time slots |
| `test_detect_time_conflicts` | Manually overlapping times are caught and typed as `time_overlap` |
| `test_recurring_task_auto_renew_on_complete` | Daily task resets and advances `start_date` by one day |
| `test_generate_plan_sessions_for_multiple_days` | Recurring task plans correctly across three consecutive days |
| `test_get_tasks_sorted_by_time_will_prioritize_by_priority_duration_and_pet` | Same-priority tasks are ordered longest-duration first |

---

## UML Class Diagram

![PawPal+ UML Diagram](Assets/Pawpal+%20Mermaid.js.png)

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the app

```bash
streamlit run app.py
```

### Usage

1. Enter an owner name, pet name, and species — click **Create Owner & Pet**.
2. Add tasks with a title, duration, priority, and frequency — click **Add task**.
3. Click **Generate schedule** to build today's plan.
4. Review the sorted schedule table, unscheduled task warnings, and any conflict details.
