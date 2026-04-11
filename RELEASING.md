# Releasing PyGets

This project is prepared for GitHub and PyPI publishing, but the actual upload still requires your GitHub repository and PyPI credentials.

## 1. Create the GitHub repository

Create a repository and push the current project:

```bash
git init
git add .
git commit -m "Initial release"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## 2. Create the PyPI project

1. Create an account on PyPI.
2. Create an API token.
3. On GitHub, add the token as repository secret `PYPI_API_TOKEN`.

## 3. Install release tooling locally

```bash
pip install -e .[dev]
```

## 4. Run validation before release

```bash
pytest tests
python -m build
python -m twine check dist/*
```

## 5. Publish a release

The repository includes a GitHub Actions workflow that publishes to PyPI when you push a tag matching `v*`.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 6. Verify installation

After the package is published:

```bash
pip install pygets
```

## Notes

- Update the version in `pyproject.toml` and `pygets/__init__.py` before each release.
- If you later know the final GitHub repository URL, add it to `pyproject.toml` under `[project.urls]`.
