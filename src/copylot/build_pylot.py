#!/usr/bin/env python3
"""
CoPylot - Customizable generator for GitHub Copilot instruction files.

This script creates a personalized copilot-instructions.md file by combining
base instructions with selected library-specific instructions.
"""

import shutil
import sys
from pathlib import Path

# Try to import questionary for interactive selection
try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False


def print_header() -> None:
    """Print a welcome header for the script."""
    print("\n" + "=" * 60)
    print(f"{' CoPylot - Copilot Instructions Generator ':=^60}")
    print("=" * 60)
    print("\nGenerate personalized GitHub Copilot instruction files for Python projects.\n")


def get_available_mods(mods_dir: Path) -> list[str]:
    """
    Get a list of available library instruction files.

    Args:
        mods_dir (Path): Path to the libraries directory.

    Returns:
        list[str]: List of available library names (without extension).
    """
    if not mods_dir.exists() or not mods_dir.is_dir():
        print(f"Error: Libraries directory not found at {mods_dir}")
        sys.exit(1)

    available_mods = []
    for file in mods_dir.glob("*.md"):
        if file.is_file():
            available_mods.append(file.stem)

    return sorted(available_mods)


def interactive_select(available_mods: list[str]) -> list[str]:
    """
    Use questionary to create an interactive checklist for library selection.

    Args:
        available_mods (list[str]): List of available libraries.

    Returns:
        list[str]: List of selected library names.
    """
    if not available_mods:
        print("No library instruction files found. Only base instructions will be included.")
        return []

    choices = [
        {"name": mod, "checked": False}
        for mod in available_mods
    ]

    try:
        selected = questionary.checkbox(
            "Select libraries to include (use arrow keys to navigate, space to select/deselect):",
            choices=choices
        ).ask()

        return selected or []
    except Exception as e:
        print(f"Error with interactive selection: {e}")
        # Fallback to text-based selection
        return fallback_select(available_mods)


def fallback_select(available_mods: list[str]) -> list[str]:
    """
    Prompt the user to select which libraries to include using text input.

    Args:
        available_mods (list[str]): List of available libraries.

    Returns:
        list[str]: List of selected library names.
    """
    if not available_mods:
        print("No library instruction files found. Only base instructions will be included.")
        return []

    print("\nAvailable libraries:")
    for i, mod in enumerate(available_mods, 1):
        print(f"{i}. {mod}")

    print("\nSelect libraries to include (comma-separated numbers, 'all' for all, or 'none' for none):")
    selection = input("> ").strip().lower()

    if selection == 'all':
        return available_mods
    if selection == 'none':
        return []

    try:
        # Parse comma-separated indices
        selected_indices = [int(idx.strip()) for idx in selection.split(',') if idx.strip()]
        # Validate indices and convert to library names
        selected_mods = [available_mods[idx - 1] for idx in selected_indices if 1 <= idx <= len(available_mods)]
        return selected_mods
    except ValueError:
        print("Invalid selection. Please enter numbers separated by commas.")
        return fallback_select(available_mods)


def select_libraries(available_mods: list[str]) -> list[str]:
    """
    Select which libraries to include, using interactive mode if available.

    Args:
        available_mods (list[str]): List of available libraries.

    Returns:
        list[str]: List of selected library names.
    """
    if HAS_QUESTIONARY:
        return interactive_select(available_mods)
    print("\nNote: For a better experience with an interactive checklist interface, install 'questionary':")
    print("      pip install questionary")
    print("      or use: python -m pip install questionary")
    return fallback_select(available_mods)


def read_markdown_file(file_path: Path) -> str:
    """
    Read the contents of a markdown file.

    Args:
        file_path (Path): Path to the markdown file.

    Returns:
        str: Contents of the file.
    """
    try:
        with Path.open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
        return ""


def generate_instructions(base_dir: Path, mods_dir: Path, selected_mods: list[str]) -> str:
    """
    Generate the copilot instructions by combining base and selected library instructions.

    Args:
        base_dir (Path): Path to the base instructions directory.
        mods_dir (Path): Path to the libraries directory.
        selected_mods (list[str]): List of selected library names.

    Returns:
        str: Combined instructions content.
    """
    # Start with the base instructions
    universal_content = read_markdown_file(base_dir / "universal.md")
    py_core_content = read_markdown_file(base_dir / "py_core.md")

    # Combine base instructions
    combined_content = f"{universal_content}\n\n{py_core_content}\n"

    # Add a section for library-specific instructions if any are selected
    if selected_mods:
        combined_content += "\n## Library-Specific Instructions\n\n"

        # Add each selected library's instructions
        for mod in selected_mods:
            lib_content = read_markdown_file(mods_dir / f"{mod}.md")
            if lib_content:
                combined_content += f"{lib_content}\n\n"

    return combined_content


def save_instructions(content: str, output_path: Path) -> None:
    """
    Save the generated instructions to a file.

    Args:
        content (str): The instruction content to save.
        output_path (Path): Path to save the file to.
    """
    output_file = output_path / "copilot-instructions.md"

    # Backup existing file if it exists
    if output_file.exists():
        backup_file = output_path / "copilot-instructions.md.bak"
        shutil.copy2(output_file, backup_file)
        print(f"Backed up existing file to {backup_file}")

    # Write the new file
    with Path.open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"\nSuccessfully generated instructions at {output_file}")


def main() -> None:
    """Main function to run the script."""
    print_header()

    # Define paths
    script_dir = Path(__file__).parent.parent.parent.resolve()  # Navigate up from src/copylot to root
    base_dir = script_dir / "src" / "uni"  # Updated path to base files
    mods_dir = script_dir / "src" / "mods"  # Updated path to library files

    # Get available libraries
    available_mods = get_available_mods(mods_dir)

    # Prompt user to select libraries
    selected_mods = select_libraries(available_mods)

    if selected_mods:
        print(f"\nGenerating instructions with: {', '.join(selected_mods)}")
    else:
        print("\nGenerating instructions with base content only.")

    # Generate and save instructions
    instructions = generate_instructions(base_dir, mods_dir, selected_mods)
    save_instructions(instructions, script_dir)

    print("\nDone! You can now copy the contents of copilot-instructions.md to your project.")
    print("Alternatively, you can add it to your .vscode/settings.json file.")


if __name__ == "__main__":
    main()
