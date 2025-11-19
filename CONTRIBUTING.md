# Dev Workflow & Git Conventions

## Branches

- `main`:
  - Always stable and green.
  - All tests and linters must pass before merging.
  - Used as the base for releases/tags.

- `feature/...`:
  - One branch per feature or issue.
  - Examples:
    - `feature/mf-core`
    - `feature/http-api`
    - `feature/evaluation-rmse`
  - Branches are short-lived and deleted after merge.

## Typical Flow

1. Update main:
   ```
   git checkout main
   git pull origin main
   ```

2. Create a feature branch:
   ```
   git checkout -b feature/<short-feature-name>
   ```

3. Develop on the feature branch:
   - Write code in `src/`.
   - Add/update tests in `tests/`.
   - Run:
     ```
     make test
     make lint
     ```

4. Commit changes with a descriptive message:
   ```
   git add .
   git commit -m "Short, clear description of the change"
   ```

5. Push and open a Pull Request (even when solo):
   ```
   git push -u origin feature/<short-feature-name>
   ```
   - Open a PR `feature/...` → `main`.
   - Ensure CI is green (tests + linters).
   - Review your own diff before merging.

6. Merge and clean up:
   - Merge the PR into `main`.
   - Delete the feature branch on GitHub (and locally if needed).

## Coding Conventions

- Follow PEP8 style.
- Use `ruff` to enforce style:
  - `make lint` → static analysis (ruff).
  - `make format` → auto-format (ruff format or black).
- Public functions/classes (part of the library API) must have docstrings:
  - Brief one-line summary.
  - Optional details on parameters and return values.

## Commit Messages

- Use short, descriptive messages in the imperative form:
  - `Add matrix factorization training loop`
  - `Implement recommend() for top-k items`
  - `Add RMSE evaluation and tests`

- Avoid vague messages:
  - `fix stuff`, `update`, `changes`.