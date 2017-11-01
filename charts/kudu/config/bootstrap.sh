#! /bin/bash

DEFAULT_KUDU_OPTS="-logtostderr \
 -fs_wal_dir=/var/lib/kudu/$1 \
 -fs_data_dirs=/var/lib/kudu/$1 \
 -use_hybrid_clock=false"

KUDU_OPTS=${KUDU_OPTS:-${DEFAULT_KUDU_OPTS}}

if [ "$1" = 'master' ]; then
  exec kudu-master -fs_wal_dir /var/lib/kudu/master ${KUDU_OPTS}
elif [ "$1" = 'tserver' ]; then
  exec kudu-tserver -fs_wal_dir /var/lib/kudu/tserver \
  -tserver_master_addrs ${KUDU_MASTER} ${KUDU_OPTS}