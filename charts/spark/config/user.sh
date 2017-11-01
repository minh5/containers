#! /bin/bash
USER_HOME="/home/user"
useradd -m -s /bin/bash -N -u 1000 user
groupadd supergroup
usermod -a -G supergroup user