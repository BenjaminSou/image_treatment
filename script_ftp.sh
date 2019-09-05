#!/bin/sh
USERNAME="synftp"
PASSWORD="ftpsyn!"
SERVER="synapse"

# local directory to pickup *.tar.gz file
FILE="files/final"

# remote server directory to upload backup
BACKUPDIR="/poubelle_ia"

# login to remote server
ftp -n -i $SERVER <<EOF
user $USERNAME $PASSWORD
cd $BACKUPDIR
mput $FILE/*.tar.gz
quit
EOF
