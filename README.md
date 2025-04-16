# CoPylot

Customizable generator for making `copilot-instructions.md` files focused on modern Python development.

## Installation

```bash
git clone https://github.com/RPINerd/CoPylotInstructions
cd CoPylotInstructions
```

### Using UV (Recommended)

This project uses [UV](https://github.com/astral-sh/uv) for dependency management and packaging.

```bash
# Install UV if you don't have it yet
pip install uv

# Install dependencies using UV
uv pip install -e .
```

### Using regular pip

```bash
pip install -e .
```

## Usage

Run the interactive script:

```bash
python build_pylot.py
```

Or if you installed as a package:

```bash
copylot
```

### Output

The script will generate a `copilot-instructions.md` file in the current directory.

Universal and python core contents will be inserted as heading information and then appended by the user selected components.

### Customization

Upon launching the script, you will be prompted to select the components you want to include in your `copilot-instructions.md` file. The current available components are:

- [Flask](./libs/flask.md)
- [NumPy](./libs/numpy.md)
- [Pandas](./libs/pandas.md)
- [Pygame](./libs/pygame.md)

## Contributing

My goal is to support as many python tech stacks as possible. Please open a PR if you want to add a new component or improve the existing ones!
