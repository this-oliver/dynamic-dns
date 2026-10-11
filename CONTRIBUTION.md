# Contribution Guideline

## Getting started

Prerequisites:

- Python 3.12 or higher

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Continous Integration

### Commit Messages

Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) guideline to make it easier for others to understand what changes were made. The format of a commit message is as follows:

```bash
git commit -m '<type>(<scope>): <description>'
```

- `<type>`: The type of change being made. There are four main types: `feat` is for new features, `fix` is for bug fixes, `docs` is for updating documentation and `chore` is for other changes that do not affect the core functionality of the project.
- `<scope>`: The scope of the project. This is an optional field that adds context to the area where the change occured.
- `<description>`: A brief description of the change.

The `<type>` is important because it dictates which semantic version of the project should be incremented.

| type                  | semver | outcome        |
| --------------------- | ------ | -------------- |
| docs, chore           | -      | 0.0.1 -> 0.0.1 |
| fix                   | patch  | 0.0.1 -> 0.0.2 |
| feat                  | minor  | 0.0.1 -> 0.1.0 |
| !feat, !fix, BREAKING | major  | 0.0.1 -> 1.0.0 |

[Commitlint](https://commitlint.js.org/) is used to ensure that the commit messages follow the conventional commit format as explained in the [commit messages](#commit-messages) section. The commitlint is configured in [.commitlintrc](./.commitlintrc) and the checks are triggered in the [.github/workflows/ci.yaml](./.github/workflows/ci.yaml) workflow.

### Testing

Testing lets us sleep better at night which is why you should test all the changes that you add to the repository.

The `pytest` framework is used against the tests found in [/tests](./tests). These tests are run on all pull requests towards the `main` branch (see [.github/workflows/ci.yaml](./.github/workflows/ci.yaml)) but you can also run the tests locally with the following command:

```bash
python3 -m pytests /tests
```

### Security Scanning

This repository scans for several security vulnerabilities that can be introduced dduring development using open source security scanning tools.

- [Trivy](https://trivy.dev/docs/latest/getting-started/) is used to scan for vulnerabl dependencies, configurations, and hard-coded credentials in the source code.

| Vulnerability                        | What is it?                               | Why is it bad?                                                                                                    | Tools             |
| ------------------------------------ | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------- |
| **Vulnerable Dependencies**          | Using outdated or flawed software parts.  | Allows attackers to exploit known weaknesses which can lead to system takeover, data theft, application crash.    | Trivy, Dependabot |
| **Hardcoded Credentials/Secrets**    | Storing passwords/keys directly in code.  | Makes it easy for attackers to find them which can lead to account hijacking, data breaches, unauthorized access. | Trivy             |
| **Misconfigured or Vulnerable Code** | Mistakes in how the application is built. | Creates entry points for attackers which can lead to data breaches, application crashes, remote control.          | Trivy             |

## Continous Deployment

### Releases

This repository uses the [release-please-action](https://github.com/googleapis/release-please-action) action to prepare a pull request with a summary of changes and title that looks like this - "Release vX.X.X". Once you are satisfied with all your changes, you can merge the pull request to create a release. This entire process is managed through the [.github/workflows/cd.yaml](./.github/workflows/cd.yaml) workflow which is triggered after changes are pushed to the `main` branch.

### Building

The dynamic dns tool is compiled into a container image so that it can be used in a consistent manner accross a majority of devices and architectures. We build the official image in [.github/workflows/cd.yaml](./.github/workflows/cd.yaml) however you can also build the container image locally:

```bash
podman build -t this-oliver/dynamic-dns:local .
```

We currently support the following platforms:

- `linux/amd64`
- `linux/arm64`
- `linux/arm/v7`
- `linux/arm/v6`
