#!/bin/sh
#***********************************************************************
# easy to run python xxx.py
# param : script name
#***********************************************************************
project_dir=${PWD}/../
cd $project_dir
export PYTHONPATH=$PYTHONPATH:$project_dir
log_dir=/var/log
script_dir=${project_dir}/eve/script
if [ $# -lt 1 ]; then
    echo missing param :script name
else
    echo $*
    /usr/bin/python ${script_dir}/$1.py >>$log_dir/eve_script_$1_$(date "+%Y%m%d").log 2>&1 &
fi
