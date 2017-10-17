#! /bin/bash

# installing gosu
export GOSU_VERSION=1.10
set -x \
dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
rm -r /usr/local/bin/gosu.asc \
chmod +x /usr/local/bin/gosu \
gosu nobody true

# configuring user
useradd -m -s /bin/bash -N -u 1000 user
USER_HOME="/home/user"
groupadd supergroup
usermod -a -G supergroup user