#!/bin/sh
#
# install configuration's file 
#
#

LOOLMONIT_FOLDER=/opt/loolmonitor


mkdir $LOOLMONIT_FOLDER/
cp conf/* $LOOLMONIT_FOLDER/
chown root.root $LOOLMONIT_FOLDER/*
chmod 600 /opt/loolmonitor/*
