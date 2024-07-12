#!/bin/bash
# coding: utf-8

echo "### Welcome to OsSitter uninstaller for version 1.1"
echo "Compatible OsSitter v5.x/4.x"

systemctl stop ossitter.service
systemctl status ossitter.service
systemctl disable ossitter.service

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
