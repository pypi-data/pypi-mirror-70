# Python Gitlab Management

[![Pipelien Status - Stable](https://img.shields.io/badge/dynamic/json.svg?label=Pipeline-Stable&query=0.status&url=https://gitlab.com/api/v4/projects/19099644/pipelines?ref=master&color=ff782e&logo=gitlab&style=plastic)](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/) 
[![Pipelien Status - Dev](https://img.shields.io/badge/dynamic/json.svg?label=Pipeline-Dev&query=0.status&url=https://gitlab.com/api/v4/projects/19099644/pipelines/?ref=development&color=ff782e&logo=gitlab&style=plastic)](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/) 
![PyPi Version](https://img.shields.io/badge/dynamic/json?label=PyPi%20Package&query=$.info.version&url=https://pypi.org/pypi/gitlab-management/json&logo=python&logoColor=white&style=plastic) 
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-green.svg?style=plastic&logo=gnu&logocolor=white)](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/blob/master/LICENCE)
[![Read the Docs (version)](https://img.shields.io/readthedocs/python-gitlab-management/stable?label=Docs%20stable&logo=readthedocs&style=plastic)](https://python-gitlab-management.readthedocs.io/en/stable/)
[![Read the Docs (version)](https://img.shields.io/readthedocs/python-gitlab-management/development?label=Docs%20devel&logo=readthedocs&style=plastic)](https://python-gitlab-management.readthedocs.io/en/development/)

Gitlab-management is python module that enables GitLab group configuration from code. By design it's intended to be setup to run on a schedule. 

## How to Use
GitLab-Management can be used from the command line or imported as a python module.

Feature wise this module only process labels (create/add). over time features will be added. please see the milestones, issue and merge requests at the home page.

For please refer to the docs.


### Python Module
To install run `pip install gitlab-management`. from there you will be able to use and extend the module as you see fit.

### CLI
Gitlab-management can be used via cli with command `python3 -m gitlab-management -H {GITLAB_URL} -T {GITLAB_PRIVATE_TOKEN}` replacing `{GITLAB_URL}` with the gitlab url and `{GITLAB_PRIVATE_TOKEN}` with your gitlab private token. to view all available options, use switch `-h` or `--help`

### Config File
The configuration file for this module (`config.yml`) is a yml formated file that is required to be in the directory that the command is ran from.

The layout of the yml file
``` yaml
Group:
    Labels:
        -
            Group: Example1
            Name: Bug
            Description: "Items that are bugs or bug related"
            Color: "#FF0000"

        -
            Group: 
                - Example1
                - Example2
            Name: Feature
            Description: "Items that are feature related"
            Color: "#00FF00"

```

`Group.Labels` is a `list` of `dict` for each label that is to be created add a new `dict` to the `list` under `Group.Labels`

`Group.Labels.#.Group` can be a single string which is the name of an existing group that the user has access to as maintainer. `Group.Labels.#.Group` can also be a `list` of group names that the label will be added to.


## Issues, Feature Requests and Bugs
If an issue or bug is found within the package (i.e. exception), please [create an issue ticket](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues) using the applicable issue template available at the time of ticket creation. If you would like to request a feature and are unable to contribute, [please create an issue](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues) using the feature issue template.

## Contributing
Contribution guide can be viewed in the [repo.](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/blob/master/CONTRIBUTING.md)


## Licence
The package licence can be viewed in the [repo](https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/blob/master/LICENSE)