import json
import os

TASKS_FILE = "data/tasks.json"

def load_tasks():
    """Load tasks from tasks.json"""

    if not os.path.exists(TASKS_FILE):
        return []

    with open(TASKS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Save tasks to tasks.json"""

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(task):
    """
    Add a new task.
    """

    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "task": task,
        "completed": False
    }

    tasks.append(new_task)

    save_tasks(tasks)

    return f"✅ Task added: {task}"

def show_tasks():
    """
    Display all saved tasks.
    """

    tasks = load_tasks()

    if not tasks:
        return "No tasks found."

    output = ""

    for task in tasks:

        status = "✓" if task["completed"] else " "

        output += f'{task["id"]}. [{status}] {task["task"]}\n'

    return output

def complete_task(task_id):
    """
    Mark a task as completed.
    """

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            if task["completed"]:
                return "Task already completed."

            task["completed"] = True
            save_tasks(tasks)

            return f"✅ Task {task_id} completed."
    return "Task not found."

def delete_task(task_id):
    """
    Delete a task by its ID.
    """

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            # Reassign IDs
            for index, task in enumerate(tasks, start=1):
                task["id"] = index

            save_tasks(tasks)

            return f"🗑️ Task {task_id} deleted."

    return "Task not found."

def update_task(task_id, new_task):
    """
    Update an existing task.
    """

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            task["task"] = new_task

            save_tasks(tasks)

            return f"✏️ Task {task_id} updated."

    return "Task not found."

def task_manager(task):

    task_lower = task.lower()

    # Add Task
    if "add" in task_lower:

        task_name = (
            task
            .replace("Add task:", "")
            .replace("add task:", "")
            .replace("Add task", "")
            .replace("add task", "")
            .strip()
        )

        return add_task(task_name)

    # Complete Task
    elif "complete" in task_lower or "completed" in task_lower:

        numbers = [int(word) for word in task.split() if word.isdigit()]

        if not numbers:
            return "Please provide a task number."

        return complete_task(numbers[0])

    # Show Tasks
    elif "show" in task_lower:

        return show_tasks()

    # Delete Task
    elif "delete" in task_lower:

        numbers = [int(word) for word in task.split() if word.isdigit()]

        if not numbers:
            return "Please provide a task number."

        return delete_task(numbers[0])

    # Update Task
    elif "update" in task_lower:

        numbers = [int(word) for word in task.split() if word.isdigit()]

        if not numbers:
            return "Please provide a task number."

        task_id = numbers[0]

        new_task = (
            task
            .replace("Update task", "")
            .replace("update task", "")
            .replace(str(task_id), "")
            .replace("to", "")
            .strip()
        )

        return update_task(task_id, new_task)

    else:
        return "Unknown task operation."