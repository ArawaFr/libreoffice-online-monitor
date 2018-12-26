#!/bin/bash
#
# install systemV init script
#
#

SYSTD=/etc/systemd/system
LOOL_MONIT_SERVICE=loolmonitor.service

echo
echo "installing systemd : " $LOOL_MONIT_SERVICE
echo "-------------------------------------------------------------"
cp systemd/$LOOL_MONIT_SERVICE $SYSTD/
chmod 644 $SYSTD/$LOOL_MONIT_SERVICE

echo
echo "systemd daemon-reload ... " 
echo "-------------------------------------------------------------"
systemctl daemon-reload



echo
echo "systemd enable : " $LOOL_MONIT_SERVICE
echo "-------------------------------------------------------------"
systemctl enable $LOOL_MONIT_SERVICE
echo
systemctl is-enabled $LOOL_MONIT_SERVICE

echo
echo "systemd status : " $LOOL_MONIT_SERVICE
echo "-------------------------------------------------------------"
systemctl status $LOOL_MONIT_SERVICE


echo
echo
