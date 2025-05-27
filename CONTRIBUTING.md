## Introduction

This project uses several tools to enhance developer collaboration and ensure high code quality.

- [uv](https://github.com/astral-sh/uv): Dependency and virtual environment management.
- [Black](https://github.com/psf/black): Enforces consistent code formatting.
  - Different developers may have different habits (or no habits at all!) in code formatting. This can not only lead to frustration, but also waste valuable time, especially with poorly formatted code. Black solves this problem by applying a common formatting. It promises that any changes it makes will **not** change the resulting byte-code.
- [µsort](https://github.com/facebook/usort): Safe, minimal import sorting for Python projects.
- [Flake8](https://flake8.pycqa.org/): Linter for identifying syntax and style errors.
  - Black will prevent linter errors related to formatting, but these are not all possible errors that a linter may catch.
- [Pre-commit](https://pre-commit.com/): Git hooks for automated code quality checks.
  - Git supports [hooks](https://git-scm.com/docs/githooks)—programs that can be run at specific points in the workflow, e.g., when `git commit` is used. The `pre-commit` hook is particularly useful for running programs like the ones above automatically. This not only helps to keep the commit history cleaner, but, most importantly, saves time by catching trivial mistakes early.

## Best practices

- **Do not commit to `main` directly**. Please use [feature branches](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) and [pull requests](https://help.github.com/articles/about-pull-requests/). Only urgent fixes that are small enough may be directly merged to `main` without a pull request.

- **Rebase regularly**. If your feature branch has conflicts with `main`, you will be asked to rebase it before merging. Getting into the habit of [rebasing](https://git-scm.com/docs/git-rebase) your feature branches on a regular basis while still working on them will save you from the hassle of dealing with massive and probably hard-to-deal-with conflicts later.

- **Avoid merge commits when pulling**. If you made local commits on a branch, but there have also been new commits to it on GitHub, you will not be able to pull the branch cleanly (i.e., fast-forward it). By default, Git will try to incorporate the remote commits to your local branch with a merge commit. Do **not** do this. Either use `git pull --rebase` or run the following to change the default:

For the current repo only:
```sh
git config pull.rebase true
```

For all Git repos on this system:
```sh
git config --global pull.rebase true
```

## Tool requirements

You will need working Python and `uv`. For Python, the recommended way of handling different Python versions is directly via `uv`. This setup greatly simplifies tool management compared to older practices we used with Poetry, `pyenv{,-win}`, `pipx`, and `scoop`.

### UNIX-like systems

Install `uv` through your package manager, e.g., on Arch Linux:
```sh
pacman -Syu python-uv
```

See the [documentation](https://docs.astral.sh/uv/getting-started/installation/) for other possible methods to install `uv`.

### Windows

> Assuming you have 64-bit Windows, **PowerShell** means "Windows PowerShell", **not** "Windows PowerShell (x86)" or "Windows PowerShell ISE". If you can't find it in the Start menu, try searching for it. All modern Windows versions install PowerShell by default. You shouldn't need to install it separately.

> PowerShell should be run as a regular user, **not** "as administrator".

In **PowerShell** run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Start developing

```sh
git clone git@github.com:ideaconsult/templates-api.git
```
```sh
cd templates-api
```
```sh
uv sync
```
```sh
uv run pre-commit install
```

## Running the formatters & linters

**IMPORTANT**: This is run automatically against the changed files on `git commit`. If hooks like `usort` or `black` fail and change some files, review the changes with `git diff` and add the changed files with `git add`. Then either run `git commit` or `uv run pre-commit` again, depending on what you were doing.

Run against changed files:
```sh
uv run pre-commit
```

Run against all files:
```sh
uv run pre-commit run --all-files
```

## Running the tests & coverage report

Run tests:
```sh
uv run pytest
```

Run tests with coverage report:
```sh
uv run pytest --cov
```

## Using specific Python versions

Run a command (e.g., `pytest`) with specific Python version:
```sh
uv run -p 3.10 pytest
```

Note that `uv` automatically downloads the required Python version.

Reinstall/upgrade all installed Python versions:
```sh
uv python install --reinstall
```

Consult the [documentation](https://docs.astral.sh/uv/guides/install-python/) for more Python-related commands.

## Specific IDE/editor notes

For Visual Studio Code it is recommended to use “Git Bash” for terminal. It is **not** recommended to activate the virtual environment for the terminal; use `uv run` instead.
