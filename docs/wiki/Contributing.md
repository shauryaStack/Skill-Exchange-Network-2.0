# Contributing

Thank you for your interest in contributing to **Skill Exchange Network 2.0**! This page explains how to set up a development environment, the branching strategy, coding conventions, and the process for submitting changes.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/Skill-Exchange-Network-2.0.git
   cd Skill-Exchange-Network-2.0
   ```
3. Follow the [Installation & Setup](Installation-and-Setup.md) guide to get the project running locally.
4. Create a new branch for your work (see [Branching Strategy](#branching-strategy) below).

---

## Branching Strategy

| Branch type | Name pattern | Example |
| :--- | :--- | :--- |
| Feature | `feature/<short-description>` | `feature/add-skill-search` |
| Bug fix | `fix/<short-description>` | `fix/login-redirect-loop` |
| Documentation | `docs/<short-description>` | `docs/update-api-reference` |
| Refactor | `refactor/<short-description>` | `refactor/notification-utils` |

Always branch off from `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

---

## Making Changes

- Keep changes **focused** — one feature or fix per branch.
- Write clear, descriptive **commit messages** in the imperative mood:
  ```
  Add skill search filter to browse page
  Fix login redirect when next param is missing
  ```
- If your change modifies a database model, add a migration:
  ```bash
  python manage.py makemigrations
  ```
  Commit the migration file alongside your code changes.

---

## Code Style

This project follows standard Django conventions:

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/). Keep lines under 100 characters.
- **Comments**: Use docstrings for every function and class. Add inline comments to explain non-obvious logic.
- **Templates**: Keep templates DRY by extending `base.html` and using template tags.
- **Views**: Keep view functions short. Move complex logic into helper functions or `utils.py`.
- **Models**: Use `verbose_name` and `verbose_name_plural` in every model's `Meta` class.

---

## Running Tests

```bash
python manage.py test core
```

Add tests for any new functionality in `core/tests.py`. Tests should cover:

- Model behaviour (creation, constraints, `__str__` methods)
- View responses (correct status codes, redirects, context data)
- API endpoints (correct JSON responses, error handling)

---

## Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a **Pull Request** against the `main` branch of the original repository.
3. Fill in the PR template:
   - **What** does this change do?
   - **Why** is it needed?
   - **How** was it tested?
   - Link any related issues (e.g., `Closes #42`).
4. Wait for a review. Address any requested changes with additional commits on the same branch.

---

## Reporting Bugs

Open an [Issue](https://github.com/shauryapradhan546/Skill-Exchange-Network-2.0/issues) with:

- A clear title describing the problem
- Steps to reproduce the bug
- Expected behaviour vs. actual behaviour
- Your environment (OS, Python version, browser if relevant)
- Any relevant error messages or screenshots

---

## Suggesting Features

Open an [Issue](https://github.com/shauryapradhan546/Skill-Exchange-Network-2.0/issues) with the label **enhancement** and describe:

- The problem the feature would solve
- Your proposed solution
- Any alternative solutions you have considered

---

## Security Vulnerabilities

Please **do not** open a public issue for security vulnerabilities. See [SECURITY.md](../../SECURITY.md) for the responsible disclosure process.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project. See [LICENSE](../../LICENSE) for details.
