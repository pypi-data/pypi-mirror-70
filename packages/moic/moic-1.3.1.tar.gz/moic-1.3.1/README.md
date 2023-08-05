# MOIC : My Own Issue CLI

> Freely inspired by https://pypi.org/project/jira-cli/

Command line inteface to interact with issue manager such as Jira, Gitlab, etc...

**Highlights**
* Modern CLI based on [Click](https://click.palletsprojects.com/en/7.x/) and [Rich](https://github.com/willmcgugan/rich)
* Context management
* Multiple tracker plugin
* Uniformed display

## Getting Started

* Install moic
```bash
> pip install moic
```

* Configure moic
```bash
> moic configure
```

* Commands
```bash
> moic
Usage: moic [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  config    Configure Jira cli, setting up instance, credentials etc...
  issue     Create, edit, list Jira issues
  list      List projects, issue_types, priorities, status
  rabbit    Print an amazing rabbit: Tribute to @fattibenji...
  sprint    Create, edit, list Jira Sprints
  template  List, edit templates
  version   Provide the current moic installed version
```

## Contribute

Feel free [open issues on Gitlab](https://gitlab.com/brice.santus/moic/-/issues) or propose Merge Requests

## Documentation

Full documentation is available at https://moic.readthedocs.io/en/latest/
