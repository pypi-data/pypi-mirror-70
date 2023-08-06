#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=v100
fi;

password=xiaomi
cloudml dev create -n $name -p $password \
--priority_class guaranteed \
-d cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:33103tql2dev  \
-cm rw \
-c 32 -M 60G \
-g 1 -gt v100 -gm 32g

