# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands
- Setup environment: `./setup_env.sh`
- Generate synthetic data: `python generate_org_data.py`
- Run analysis notebook: `jupyter notebook analyze_org_data.ipynb`

## Code Style Guidelines
- Follow PEP 8 conventions for Python code
- Use type hints for function signatures
- Maximum line length of 88 characters (Black default)
- Use f-strings for string formatting
- Write comprehensive docstrings for functions and classes
- Use clear, descriptive variable and function names
- Organize imports: standard library first, then third-party, then local modules
- Prefer pandas vectorized operations over loops when working with dataframes
- For data visualization, maintain consistent styling (seaborn whitegrid, ggplot)
- Handle errors explicitly with try/except blocks when appropriate
- Use constants for configuration values at the top of files