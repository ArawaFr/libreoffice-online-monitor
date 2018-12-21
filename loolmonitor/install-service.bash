#!/bin/sh
#
# install systemV init script
#
#

INIT_D=/etc/rc.d/init.d
LOOL_MONIT_SERVICE=loolmonitor


cp service/$LOOL_MONIT_SERVICE $INIT_D/
chmod 744 $INIT_D/$LOOL_MONIT_SERVICE
chkconfig --add $LOOL_MONIT_SERVICE
chkconfig --list $LOOL_MONIT_SERVICE
