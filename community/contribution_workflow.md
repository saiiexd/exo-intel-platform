# Contribution Workflow

Thank you for your interest in contributing to the ExoIntel AI Exoplanet Discovery Platform! We welcome contributions from astrophysicists, data scientists, and software engineers alike.

To ensure a smooth collaboration process, please follow the workflow outlined below.

## 1. Fork the Repository

1. Navigate to the top right of the ExoIntel repository on GitHub and click the **"Fork"** button.
2. Clone your newly forked repository to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/exo-intel-platform.git
   cd exo-intel-platform
   ```

## 2. Create a Branch

Never commit directly to the `main` branch. Always create a descriptive feature branch for your work.

```bash
# For a new feature
git checkout -b feature/your-feature-name

# For a bug fix
git checkout -b fix/issue-description

# For documentation updates
git checkout -b docs/update-methodology
```

## 3. Make Your Changes

*   **Code Standards:** ExoIntel follows PEP 8 for Python backend code and ESLint/Prettier for the React frontend.
*   **Documentation:** If adding a new feature (e.g., a new Astrophysical Feature in the engineering step), ensure you update `research/dataset_description.md` accordingly.
*   **Tests:** If adding complex ML logic, please include corresponding unit tests in a `tests/` directory (if applicable).

## 4. Commit Your Changes

Write clear, concise commit messages. A good commit message explains *what* changed and *why*.

```bash
git add .
git commit -m "Add Density Ratio engineered feature to ML pipeline"
```

## 5. Keep Your Fork Updated

Before pushing, ensure your branch is up-to-date with the upstream repository to avoid merge conflicts.

```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/exo-intel-platform.git
git fetch upstream
git rebase upstream/main
```

## 6. Push to Your Fork

Push your changes up to your GitHub fork:

```bash
git push -u origin feature/your-feature-name
```

## 7. Submit a Pull Request

1. Go to the original ExoIntel repository.
2. Click **"Compare & pull request"**.
3. Fill out the Pull Request template comprehensively. Include context on the scientific or technical motivations behind your change.
4. Request review from a core maintainer.

Once approved, your changes will be merged into the main discovery pipeline!
