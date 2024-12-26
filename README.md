# StateSync utility

This utility implements a [GitOps](https://www.redhat.com/en/topics/devops/what-is-gitops) approach for managing OS packages and settings.

Of course, I know about [Ansible]([https://](https://www.redhat.com/en/ansible-collaborative)) and [Ubuntu autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html), but right now, the main goal of this repository is to learn the technologies more deeply.

## How it works

First you need to create a YAML [configuration file]([https://](https://github.com/artur-titov/state-sync/blob/master/config-example.yml)).

Following the GitOps approach, place the config file in a separate repository.

Distribution via a Deb package and sync based on a remote file are not implemented yet. However, you can clone both repositories to the target host.

After that run sync command:

```sh
make sync FROM="<path_to_config_file>"
```

The OS synchronizes with the settings entered in the configuration file.

## Tested with

- Ubuntu 24.04 LTS
- Python 3.12.3

## Roadmap

|

### Step 1

| Status    | Target    | Description   |
| :---      | :---      | :---          |
| __done__      | Basic app syncronization  | *apt, snap, flatpak* |
| __done__      | Unit tests    ||
| *in progress* | CI/CD | linter, tests |

### Step 2

| Status    | Target    | Description   |
| :---      | :---      | :---          |
| planned   | Distribute as Deb-package | For 'apt install state-sync' |

### Step 3

| Status    | Target    | Description   |
| :---      | :---      | :---          |
| backlog   | Integration tests ||
| backlog   | Gsettings  ||
| backlog   | Post commands    ||

### Step 4

| Status    | Target    | Description   |
| :---      | :---      | :---          |
| backlog   | Sync based on remote file? ||
| backlog   | Custom app synchronisation ||
| backlog   | Pull model | Settings to sync in background |

### In Future

| Status    | Target    | Description   |
| :---      | :---      | :---          |
| backlog   | Support other distributors | pacman, dnf, etc. |
| backlog   | Pull model | Settings to sync in background |

...
