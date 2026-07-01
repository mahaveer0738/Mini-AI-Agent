from agent.router import detect_route
from concurrent.futures import ThreadPoolExecutor

from agent.tools import (
    calculator,
    task_manager,
    chat,
    memory,
    extract
)

TOOLS = {
    "calculator": calculator,
    "task_manager": task_manager,
    "chat": chat,
    "memory": memory,
    "extract": extract
}

def run_agent(user_input):

    # Get execution plan from router
    plan = detect_route(user_input)

    print("\n========== EXECUTION PLAN ==========")
    print(plan)
    print("====================================\n")

    steps = plan["steps"]

    results = []

    if plan.get("parallel"):

        def execute_step(step):

            tool = step["tool"]
            tool_input = step["input"]

            return TOOLS[tool](tool_input)

        with ThreadPoolExecutor() as executor:

            results = list(executor.map(execute_step, steps))

    else:

        for step in steps:

            tool = step["tool"]
            tool_input = step["input"]

            result = TOOLS[tool](tool_input)

            results.append(result)

    return results