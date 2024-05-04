# Description

## Prerequisites

* python3
* virtualenv package

## Setup

### Setup python dependencies

1. `cd ./nexus_migration/artifacts_migration`
2. (setup once) `virtualenv -p python3 maven`
3. `source maven/bin/activate`
4. (setup once)  `pip3 install -r requirements.txt`

## Cleanup

### Delete maven virtualenv

1. `rm -r maven`