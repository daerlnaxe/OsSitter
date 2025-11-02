#!/bin/bash
# coding: utf-8

echo "### Welcome to OsSitter uninstaller for version 1.1"
echo "Compatible OsSitter v5.x/4.x"

echo "Debugging.. don't use for the while"
#stop for the while
exit0

systemctl stop ossitter.service
systemctl status ossitter.service
systemctl disable ossitter.service

# Read the install folder from the systemd service file
installFolder=$(grep -oP 'ExecStart=\S+' /etc/systemd/system/ossitter.service | sed 's|ExecStart=/bin/bash -c "cd \(.*\) && .*|\1|')

# If we can't determine the install folder, exit with error
if [[ -z "$installFolder" ]]; then
    echo "Error: Couldn't determine the installation folder from the service file."
    exit 1
fi


echo "The installation folder is: $installFolder"


echo "Removing ossitter.service"
rm /etc/systemd/system/ossitter.service
systemctl daemon-reload

echo "for the while you must delete OsSitter manually"


read -p "Enter the service account name you want to delete: " ch_user
if [[ -z "$ch_user" ]]; then
    echo "Exit : no user selected"
	exit 1
fi

set -e
id $ch_user

read -p "Are you sure you want delete $ch_user ?(y/*) " res
if [[ $res=="y" ]]
then
	userdel $ch_user
fi
