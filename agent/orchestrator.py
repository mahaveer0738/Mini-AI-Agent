from agent.router import detect_route

from agent.tools import (
    calculator,
    task_manager,
    chat,
    memory
)

# Tool Registry
TOOLS = {
    "calculator": calculator,
    "task_manager": task_manager,
    "chat": chat,
    "memory": memory
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

        # (Placeholder)
        # Later we will execute these with ThreadPoolExecutor
        for step in steps:

            tool = step["tool"]
            tool_input = step["input"]

            result = TOOLS[tool](tool_input)

            results.append(result)

    else:

        for step in steps:

            tool = step["tool"]
            tool_input = step["input"]

            result = TOOLS[tool](tool_input)

            results.append(result)

    return results