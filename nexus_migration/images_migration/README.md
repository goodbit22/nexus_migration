# Descriptions

## Prerequisites

* python3
* virtualenv package

## Setup

### Setup python dependencies

1. `cd ./nexus_migration/images_migration`
2. (setup once) `virtualenv -p python3 docker`
3. `source docker/bin/activate`
4. (setup once)  `pip3 install -r requirements.txt`

## Cleanup

### Delete docker virtualenv

1. `rm -r docker`
