# StateSync

This utility synchronize your OS configuration from YAML file. 

You can manage OS packages and settings with GitOps approach.


## How it works

First you need to create a YAML [configuration file](https://github.com/artur-titov/state-sync/blob/master/config-example.yml).

Clone this repository then create venv and install requirements. After that go to the StateSync directory and run command:

```bash
# Flow supports:
#
# plan - for compare current OS state with configuration file without changes applying.
# apply - for sync configuration file settings with OS.

python state_sync {flow} ~/path/to/config.yaml
```

## Tested with

![example branch parameter](https://github.com/artur-titov/state-sync/actions/workflows/ci.yml/badge.svg?branch=development)

- Ubuntu 22.04+
- Python 3.12+
