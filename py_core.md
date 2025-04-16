## Python Code

### Core Tennants

- In general, follow PEP 8 format guidelines.
- Intendations are 4 spaces, no tabs.
- Code nesting should be minimal; preferably under 4 levels, but never more than 5.
- Unless explicity directed otherwise, build code to utilize the most recent stable Python version.
- Errors should never be silent, use exceptions to raise detailed errors.
- Minimize the use of global variables.

### Style Specifics

- Follow RUFF linting and formatting rules.
- Provide type hints for all function arguments and return types.
- Follow Google style guide for docstrings.

    ```python
    def div(a: int, b: int) -> int:
        """
        Divide two integers.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The sum of the two integers.

        Raises:
            ValueError: If the second integer is zero.
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    ```

### Standard libraries

Utilize UV where possible for managing packages and virtual environments. Prioritize standard libraries over third-party libraries unless a third-party library is significantly better.

- Use pathlib instead of os.path for file and directory manipulations.
- Use argparse for command-line argument parsing.
- Use logging instead of print statements for debugging and information messages.
- Use pytest for unit testing.
- Use itertools for advanced iterable manipulations.

### Third-party Libraries
