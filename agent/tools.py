import ast
import operator

# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def evaluate(node):
    """
    Recursively evaluate an AST node.
    """

    # Numbers (Python 3.8+)
    if isinstance(node, ast.Constant):
        return node.value

    # For older Python versions
    elif isinstance(node, ast.Num):
        return node.n

    # Binary Operations
    elif isinstance(node, ast.BinOp):

        left = evaluate(node.left)
        right = evaluate(node.right)

        operator_function = OPERATORS[type(node.op)]

        return operator_function(left, right)

    # Unary Operations (-5, +5)
    elif isinstance(node, ast.UnaryOp):

        value = evaluate(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        elif isinstance(node.op, ast.UAdd):
            return value

    raise ValueError("Unsupported mathematical expression.")


def calculator(expression):
    """
    Safely evaluate a mathematical expression using AST.
    """

    try:

        tree = ast.parse(expression, mode="eval")

        result = evaluate(tree.body)

        return f"Result: {result}"

    except ZeroDivisionError:
        return "Error: Division by zero."

    except Exception:
        return "Error: Invalid mathematical expression."


# Temporary Task Manager
def task_manager(task):
    return f"Task Manager received: {task}"