# Template

This repository is a template designed to get you started with a secure Continous Integration and Development (CI/CD) pipeline. The template includes:

- Continuous [integration](./.github/workflows/ci.yaml) and [deployment](./.github/workflows/cd.yaml) (CICD)
  - Validates commit messages using `commitlint` to ensure they follow a conventional format.
  - Checks PR titles and commits for adherence to predefined rules.
  - Automatically creates releases when changes are pushed to the `main` branch.
- Continuous security scans to identify and mititgate vulnerabilities in source code and supply chain (dependencies).
- Dependency management with [dependabot](./.github/dependabot.yaml) and [auto-merge.yaml](./.github/workflows/auto-merge.yaml) to ensure that your project is secure and up-to-date with the latest dependencies.
- Standardized feature and bug reporting with [./.github/ISSUE_TEMPLATE](./.github/ISSUE_TEMPLATE/)
- Standardized and readable commit messages with [Commitlint](./.commitlintrc).

This repository contains a set of GitHub Actions workflows designed to automate continuous integration (CI) and continuous deployment (CD) processes. The workflows are tailored to ensure that code changes adhere to specific standards and guidelines, enhancing the reliability and maintainability of the project.

## Getting Started

This repository is designed with some expectations and guidelines to ensure that code changes adhere. Read the [`CONTRIBUTION.md` file](./CONTRIBUTION.md) to understand how to use this repository effectively.
