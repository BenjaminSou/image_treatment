#!/bin/sh
USERNAME="synftp"
PASSWORD="ftpsyn!"
SERVER="synapse.meteo.fr"

# local directory to pickup *.tar.gz file
FILE="$MFDATA_CURRENT_PLUGIN_DIR/files/final"

# remote server directory to upload backup
BACKUPDIR="poubelle_ia"

cd $FILE || exit

# login to remote server
ftp -n -i $SERVER <<EOF
user $USERNAME $PASSWORD
cd $BACKUPDIR
mput *.tar
quit
EOF
