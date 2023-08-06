<!-- <p align="center">
  <a href="http://suite-api.superb-ai.com/" target="blank"><img src="logo/cool-tree.png" width="200" height="200" alt="Cool-Tree Logo" /></a>
</p> -->

# Suite CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/pypi/v/spb-cli)
![Build](https://github.com/Superb-AI-Suite/cool-tree/workflows/Build/badge.svg)
<!--![Unit Test](https://github.com/Superb-AI-Suite/cool-tree/workflows/Unit%20Test/badge.svg)-->


Official Suite SDK for managing [Superb AI Suite Platform](https://suite.superb-ai.com)

Suite SDK can both be used from the [command line interface](#usage-as-a-command-line-interface-cli) and as a [Python library](#usage-as-a-python-library).

- Installation
- Getting Started
- Listing Projects
- Uploading Dataset
- Downloading Data & Labels

## Installation

```shell
$ pip install spb-cli
$ spb --version

0.0.xx
```
Once installed, you can type `spb` command in the terminal to access the command line interface.

<!---
<img src="./install-spb-cli.gif" width="600">
-->

# Usage as a command line interface (CLI)

## Getting Started

### Authentication

<img src="./configure-cli.gif" width="600">

You need an *Access Key* for authentication. The *Access Key* can be generated on the :tada: [Superb AI Suite web](https://suite.superb-ai.com/) (Suite > My Account > Advanced).

You can then configure your profile by entering your *Suite Account Name* and the generated *Access Key*. 

:warning: ***Suite Account Name* does <ins>NOT</ins> refer to your personal account. It refers to the organization name that your personal account belongs to.**

```shell
$ spb configure
Suite Account Name: foo
Access Key: bar
```

Once configured, you can check the currently configured profile by using the `--list` option.


```
$ spb configure --list

[default]
access_key = foo
account_name = bar
```

## Listing Projects

<img src="./describe-projects.gif" width="600">

You can list all projects that belong to the currently configured profile by using the following command:
```shell
$ spb describe projects

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ NAME                                               ┃ LABELS ┃ PROGRESS ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ my-project                                         │   5837 │    13.7% │
...
Press any button to continue to the next page (1/10). Otherwise press ‘Q’ to quit.
```

## Uploading Dataset

<img src="./upload.gif" width="600">

You can upload data and create labels for your project with this command line interface. 

Move to the dataset directory that has image files (with extension of `.jpg`, `.png`, `.gif`) and upload images in the directory by using the following CLI command:

```shell
$ cd your-folder
$ spb upload dataset
Project Name: my-project
Dataset Name: sample-dataset

Uploading 3 data and 0 labels to dataset 'sample-dataset' under project 'my-project'. Proceed? [y/N]: y
Uploading data:
100%|██████████████████████████████████████████████████| 3/3 [00:03<00:00,  1.06s/it]
```

If you wish to upload the **pre-label** files along with the dataset, you can enable the `--include-label` option:

```shell
$ cd your-folder
$ spb upload dataset --include-label
Project Name: my-project
Dataset Name: sample-dataset

Uploading 3 data and 0 labels to dataset 'sample-dataset' under project 'my-project'. Proceed? [y/N]: y
Uploading data:
100%|██████████████████████████████████████████████████| 3/3 [00:03<00:00,  1.06s/it]
Uploading labels:
100%|██████████████████████████████████████████████████| 3/3 [00:03<00:00,  3.40s/it]
```

Or if you wish to only upload the **pre-label** :label: files:

```shell
$ spb upload labels
Project Name: my-project
Dataset Name: sample-dataset
```

To understand how to construct a **pre-label** JSON file according to the Superb AI format, please refer to the Superb AI Suite Manual.


## Downloading Data & Labels

<img src="./download.gif" width="600">

You can download images and labels for a project by using the following command:
```shell
$ cd your-folder
$ spb download
Project Name: my-project

Downloading 3 data and 3 labels from project 'my-project' to '.'. Proceed? [y/N]: y
100%|██████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.11it/s]

** Result Summary **
Successful download of 3 out of 3 labels. (100.0%)
Successful download of 3 out of 3 data. (100.0%)
```

The result is saved to the designated directory. For example:

```
└─ your-folder
   └─ sample-dataset
      ├─ 1.jpg
      ├─ 1.jpg.json
      ├─ 2.jpg
      ├─ 2.jpg.json
      ...
```


<!--

# Usage as a python library
### Client Authntication

To perform remote operations on Suite you first need to authenticate.
This requires a [Account-specific API-key].

To start the authentication process:

```
$ vim ~/.spb/config

[YOUR_PROFILE_NAME(Default : default)]
access_key=YOUT_ACCESS_KEY
account_name = YOUR_ACCOUNT_NAME
```
You can also directly use Access key and Account name to SDK. (Check, how to use)


### How to use

First. you need to authenticate and get client from SDK
```
# Use default profile in credentials
spb.client()

# Use other profile in credentials
spb.client(profile='OTHER_PROFILE_NAME')

# and also you can directly use account_name and access_key
spb.client(account_name='YOUR_ACCOUNT_NAME', access_key='YOUR_ACCESS_KEY')
```

Now, you can use Suite SDK in your project

#### Example #1 - Describe Project
```
import spb
from spb.command import Command
from spb.models import Project

def describe_project():
    spb.client()
    command = Command(type='describe_project')
    projects = spb.run(command=command)

if __name__ == "__main__":
    describe_project()

```
In this case, you can be seen Project list in your account


-->
