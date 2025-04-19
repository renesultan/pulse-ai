# Getting Started with Pulse AI

This tutorial will guide you through the process of setting up your development environment and making your first contribution to the Pulse AI project.

## Prerequisites

Before you begin, ensure you have the following installed:
- Git
- Python 3.8+
- PostgreSQL 13+
- Node.js 16+ (for future frontend development)

## Step 1: Fork and Clone the Repository

1. Fork the repository on GitHub by clicking the "Fork" button at the top right of the [repository page](https://github.com/renesultan/pulse-ai).

2. Clone your fork to your local machine:
   ```bash
   git clone git@github.com:YOUR_USERNAME/pulse-ai.git
   cd pulse-ai
   ```

3. Add the upstream repository as a remote:
   ```bash
   git remote add upstream git@github.com:renesultan/pulse-ai.git
   ```

## Step 2: Set Up Your Development Environment

1. Run the setup script to create a virtual environment and install dependencies:
   ```bash
   ./setup_env.sh
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Generate synthetic data for development:
   ```bash
   python generate_org_data.py
   ```

4. Verify that the data was generated correctly by checking the `synthetic_data` directory.

## Step 3: Understand the Project Structure

Take some time to familiarize yourself with the project structure:

- `docs/` - Project documentation
  - `architecture/` - Technical architecture and design
  - `development/` - Development guides and workflows
  - `tutorials/` - Tutorials like this one
- `synthetic_data/` - Generated test data
- `generate_org_data.py` - Script to generate synthetic data
- `setup_env.sh` - Environment setup script

Review the [README.md](../../README.md) for an overview of the project and its current status.

## Step 4: Explore the Technical Design

1. Read through the [architecture overview](../architecture/overview.md) to understand the system design.
2. Review the [data model documentation](../architecture/data-model.md) to understand the core entities.
3. Check the [API design](../architecture/api.md) to understand how the backend will be structured.

## Step 5: Choose a Task to Work On

1. Look at the project roadmap in the README to see what's currently being worked on.
2. Check the GitHub Issues for tasks labeled "good first issue" or ask the maintainers for suggestions.
3. Comment on an issue you'd like to work on to let others know you're tackling it.

## Step 6: Create a Feature Branch

Create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
```

Use the appropriate prefix for your branch:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `refactor/` for code refactoring

## Step 7: Make Your Changes

1. Implement your changes following the project's coding standards.
2. Add tests for your code.
3. Update documentation as needed.
4. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "feat: add user authentication service"
   ```

## Step 8: Keep Your Branch Updated

Regularly update your branch with changes from the upstream repository:

```bash
git fetch upstream
git rebase upstream/main
```

## Step 9: Submit a Pull Request

1. Push your changes to your fork:
   ```bash
   git push -u origin feature/your-feature-name
   ```

2. Go to the GitHub repository and create a Pull Request.
3. Fill out the PR template with details about your changes.
4. Wait for code review and address any feedback.

## Step 10: After Your PR is Merged

1. Update your local main branch:
   ```bash
   git checkout main
   git pull upstream main
   ```

2. Delete your feature branch:
   ```bash
   git branch -d feature/your-feature-name
   ```

3. Celebrate your contribution! 🎉

## Common Tasks

### Running Tests

Once tests are implemented, you'll be able to run them with:
```bash
pytest
```

### Exploring Data

You can explore the synthetic data using the Jupyter notebook:
```bash
jupyter notebook analyze_org_data.ipynb
```

### Getting Help

If you get stuck or have questions:
1. Check the documentation in the `docs` directory
2. Look for similar issues on GitHub
3. Reach out to the project maintainers

## Next Steps

Now that you're set up, consider:
- Reading the [development workflow](../development/workflow.md) guide for more details
- Exploring the [API design](../architecture/api.md) documentation
- Looking at the project roadmap to understand upcoming work

Happy coding!
