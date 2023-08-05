# Dell SC

## Introduction

Interacting with Dell SCs via REST API.

The project provides a command line interface (CLI) to connect to Dell Storage Manager and run basic operations, e.g., get list of volumes, servers, snapshots. It is a reimplementation of the developed functions in Shell to clone and recycle volumes, and handle filesystem devices (mount, unmount, update multipah, update fstab), etc. The original Shell implementation is on the Git repository https://git.uis.cam.ac.uk/i/uis/infra/dellsc.git.

## Running the Application
### Prerequisites
- [requests 2.22.0](https://pypi.org/project/requests/2.22.0/)
- [Python 3.6](https://www.python.org/downloads/release/python-360/)

### Installation
As `root`, run:
```bash
pip3 install ucamdsm
```
### CLI
For example, to show command help:
```bash
usage: ucamdsm [-h] [--dsm_host DSM_HOST] [--dsm_port DSM_PORT]
               [--dsm_user DSM_USER] [--dsm_password DSM_PASSWORD]
               [--is_secure IS_SECURE] [--record_config RECORD_CONFIG]
               [--file FILE]
               {list,delete_volume,replace_volume,clone_volume,create_snapshot,delete_recycled_vols,map_volume,unmap_volume}
               ...

Manage Dell Storage Manager objects via REST API.

positional arguments:
  {list,delete_volume,replace_volume,clone_volume,create_snapshot,delete_recycled_vols,map_volume,unmap_volume}
    list                List Dell SC objects. Example: ucamdsm --dsm_user user
                        --dsm_password abc123 list --object scs
    delete_volume       Delete Dell SC Volume. Example: ucamdsm --dsm_user
                        user --dsm_password abc123 delete_volume --vol_wwn
                        12345
    replace_volume      Clone the volume mounted on source mountpoint and
                        mount it on destination mountpoint. Then, delete the
                        volume was initially mounted on destination
                        mountpoint. Example: ucamdsm --dsm_user user
                        --dsm_password abc123 replace_volume --src_mp /src
                        --dst_mp /dst
    clone_volume        Create a snapshot with label of a volume with WWN,
                        create a view volume from the snapshot, then, map the
                        view volume to local server and mount it on target
                        mountpoint. Example: ucamdsm --dsm_user user
                        --dsm_password abc123 clone_volume --vol_wwn 12345
                        --replay_label test1 --target_mp /target
    create_snapshot     Create a snapshot of the volume mounted on a given
                        mountpoint. Example: ucamdsm --dsm_user user
                        --dsm_password abc123 create_snapshot --mp /mp
                        --replay_label test1 --retention 5
    delete_recycled_vols
                        Delete recycled volumes whose WWNs are listed in a
                        file. Example: ucamdsm --dsm_user user --dsm_password
                        abc123 delete_recycled_vols --wwns_file
                        /tmp/recycled_vols_wwns.txt
    map_volume          Maps the volume to local server and mounts it on the
                        specified mount point. Example: ucamdsm --dsm_user
                        user --dsm_password abc123 map_volume --wwn vol_wwn
                        --mp /d10
    unmap_volume        Unmaps the volume from local server. Volume must be
                        unmounted. Example: ucamdsm --dsm_user user
                        --dsm_password abc123 create_snapshot --wwn vol_wwn

optional arguments:
  -h, --help            show this help message and exit
  --dsm_host DSM_HOST   DSM hostname. Default: sc-data-ma.admin.cam.ac.uk
  --dsm_port DSM_PORT   DSM port. Default: 3033
  --dsm_user DSM_USER   DSM Data Collector username
  --dsm_password DSM_PASSWORD
                        DSM Data Collector password
  --is_secure IS_SECURE
                        Secure connection. Default: False
  --record_config RECORD_CONFIG
                        Record multipath and file system config details.
                        Default: False (do not record system config details)
  --file FILE           Read arguments from json file
```

Or, to get the list of Storage Centers:
```bash
$ ucamdsm --dsm_host host --dsm_user user --dsm_password password list --object scs --output json
07/10/2019 04:24:32 PM INFO Connected to DSM. API Version: 3.5, Connection ID: 0
07/10/2019 04:24:32 PM INFO API call ApiConnection/ApiConnection/0/StorageCenterList succeeded.
07/10/2019 04:24:32 PM INFO List of scs:
{
    "SB Storage Center": {
        "instanceId": "000",
        "hostOrIP": "x.x.x.x"
    },
    "WCDC Storage Center": {
        "instanceId": "000",
        "hostOrIP": "y.y.y.y"
    }
}
07/10/2019 04:24:32 PM INFO Logout of DSM: True.
```
You can get prompted for `user` and `password` if they are not specified in the command.
```bash
$ ucamdsm --dsm_host host list --object scs --output json
Username: user
Password: 
07/16/2019 04:59:53 PM INFO Connected to DSM. API Version: 3.5, Connection ID: 0
07/16/2019 04:59:53 PM INFO API call ApiConnection/ApiConnection/0/StorageCenterList succeeded.
07/16/2019 04:59:53 PM INFO List of scs:
{
    "SB Storage Center": {
        "instanceId": "000",
        "hostOrIP": "x.x.x.x"
    },
    "WCDC Storage Center": {
        "instanceId": "000",
        "hostOrIP": "y.y.y.y"
    }
}
07/16/2019 04:59:53 PM INFO Logout of DSM: True.
```
The command can also read arguments from a `json` file.

Example of a `json` file, `args.json`:
```bash
{
    "dsm_host": "abc",
    "dsm_port": 3033,
    "dsm_user": "user",
    "dsm_password": "password",
    "is_secure": false,
    "record_config": false,
    "subparser": "list",
    "object": "scs",
    "output": "json"
}
```
To read arguments from `args.json`:
```bash
$ ucamdsm --file args.json
07/16/2019 05:05:57 PM INFO Connected to DSM. API Version: 3.5, Connection ID: 0
07/16/2019 05:05:58 PM INFO API call ApiConnection/ApiConnection/0/StorageCenterList succeeded.
07/16/2019 05:05:58 PM INFO List of scs:
{
    "SB Storage Center": {
        "instanceId": "000",
        "hostOrIP": "x.x.x.x"
    },
    "WCDC Storage Center": {
        "instanceId": "000",
        "hostOrIP": "y.y.y.y"
    }
}
07/16/2019 05:05:58 PM INFO Logout of DSM: True.
```
### Application logging
All the log files related to the tasks executed with the CLI are stored in `/var/log/ucamdsm/`.

## Acknowledgments

- Project structure is mainly based on https://github.com/mrako/python-example-project 
- Some functions implementation was inspired from https://github.com/openstack/cinder
