# mdbh - A Python module and guidelines for using Sacred with MongoDB.
This repository holds mostly two purposes: 

First, it provides a Python module together with some CLI scripts to ease the 
usage of MongoDB together with [Sacred](https://github.com/IDSIA/sacred)
and [Omniboard](https://github.com/vivekratnavel/omniboard), 
filling a low-level gap. 
Whereas [Omniboard](https://github.com/vivekratnavel/omniboard) is well suited 
to  quickly explore data and compare Sacred experiments, it is not meant for
more complex data visualization and low-level database access.
This can for example be useful when preparing print-quality plots.

Second, it provides a [Wiki](https://gitlab.com/MaxSchambach/mdbh/-/wikis/home)
to collect guidelines on how to use Sacred with MongoDB, Omniboard and mdbh.
In particular, a multi-user, multi-database setup with password restriction and controlled
read/write access to multiple databases is provided. This Wiki is not meant
to be exhaustive, but shall get you started with your own setup.

>**Note:** This is still somewhat under development.


[[_TOC_]]


## Installation

>**TODO:** Deploy to PyPi

Install via PyPi using pip 
```bash
pip install mdbh
```

## Setup
The MongoDB instance configuration is done using one (or multiple) configuration
files which simply store the server IP, port and possible the username, password
and authentication methods and database names. 
See the `examples` folder for an example.

By default, it is assumed the this configuration
file can be found under
```bash 
~/.mongo.conf
```
