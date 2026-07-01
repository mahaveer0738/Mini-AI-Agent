from concurrent.futures import ThreadPoolExecutor

from agent.router import detect_route
from agent.tools import (
    calculator,
    task_manager,
    chat,
    memory,
    extract
)

# -----------------------------
# Tool Registry
# -----------------------------

TOOLS = {
    "calculator": calculator,
    "task_manager": task_manager,
    "chat": chat,
    "memory": memory,
    "extract": extract
}

# Set True only while debugging
DEBUG = False


def execute_step(step):
    """
    Execute a single tool safely.
    """

    tool = step["tool"]
    tool_input = step["input"]

    try:
        return TOOLS[tool](tool_input)

    except KeyError:
        return f"❌ Unknown tool: {tool}"

    except Exception as e:
        return (
            f"❌ Tool '{tool}' failed.\n"
            f"Reason: {str(e)}"
        )   

def run_agent(user_input):
    """
    Main Orchestrator
    """

    # Get execution plan from router
    plan = detect_route(user_input)
    if plan["intent"] == "error":
        return [plan["reason"]]

    if DEBUG:
        print("\n========== EXECUTION PLAN ==========")
        print(plan)
        print("====================================\n")

    steps = plan["steps"]

    # -----------------------------
    # Parallel Execution
    # -----------------------------

    if plan.get("parallel"):

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(execute_step, steps))

    # -----------------------------
    # Sequential Execution
    # -----------------------------

    else:

        results = []

        for step in steps:
            results.append(execute_step(step))

    return results