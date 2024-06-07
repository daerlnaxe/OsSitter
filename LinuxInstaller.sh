#!/bin/bash
# coding: utf-8

# Make me executable by using 'sudo chmod +x LinuxInstaller.sh'
# Then run me by using 'sudo ./LinuxInstaller.sh'
echo "### Welcome to OsSitter installer for version 1.1"
echo "Compatible OsSitter v4/4.1"
echo "Note: The configuration file will not be overwritten"
# stop if error

while getopts ":f:l:u:" opt; do
  # Assign
  case $opt in
    f) tar_file="$OPTARG"
    ;;
    l) lang_file="$OPTARG"
    ;;
	u) ch_user="$OPTARG"
	;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac
  # Evaluate
  #case $OPTARG in
  #  -*) echo "Option $opt needs a valid argument"
  #  exit 1
  #  ;;
  # esac
done
if [ -z "$tar_file" ] ; then
        echo 'Missing -f' >&2
        exit 1
fi


# Test tar file
set -e
echo "Test '$tar_file'"
if [[ ! -f $tar_file ]];then
	echo "This file doesn't exists: $tar_file"
	exit 10
fi

tar -tzf $tar_file > /dev/null 

if [[ $? != 0 ]]
then
	echo "This tar file is invalid: $tar_file"
	exit 11
else 
	echo "Test tar file: success"
fi

set +e



# Service account
read -p "Enter a service account name: " ch_user
if [[ -z "$ch_user" ]]; then
    echo "Exit : no user selected"
	exit 1
fi
echo "You want run it as '$ch_user'"
id $ch_user > /dev/null >&1
res=$?
set -e

if [[ $res != 0 ]]
then
useradd --system --create-home $ch_user
echo "$ch_user created"

fi

# Installation folder
installFolder="/home/$ch_user"
read -p "Current install folder is $installFolder, keep it ? (*/n)" res

if [[ $res == 'n' ]]
then
	read -p "Enter the installation folder: " installFolder
	if [[ -z "$installFolder" ]]; then
		echo "Exit : no folder selected"
		exit 1
	fi	
fi	

echo "You will install to '$installFolder'"

# Decompress
set -e
if [[ ! -d ./tmp ]]
then
	mkdir ./tmp
fi

echo "Decompressing ..."
# --Strip-components=1 remove root
tar -xzf $tar_file -C tmp --strip-components=1


# Always after Decompression
echo "language files"
i=1
declare -A arrVar
for file in ./tmp/Resources/*lang.json; do
	echo "$i) $(basename ${file})"
	arrVar[$i]=${file}

	i+=1
done

read -p "Select a language: " languageRow
languageFile=${arrVar[$languageRow]}


if [[ -z "$languageFile" ]]; then
    echo "Exit : no language selected"
	exit 1
fi

echo "You selected the '$(basename $languageFile)' file"

read -p "Press a key to continue"


# Move files
echo "Move files to installation folder $installFolder"
mkdir -p $installFolder
fullIF=$(realpath $installFolder)

cd $fullIF || exit 1
cd - > /dev/null

for file in ./tmp/*.py;
do
	echo "--- moving ${file}";
	sudo mv ${file} $fullIF
done

sudo cp $languageFile $fullIF/currentlang.json

# Stop if error
# PrincipeExecStart=/bin/bash -c 'cd /home/ubuntu/project/ && python app.py'
sed -i "s,{InstallFolder},$fullIF,gm" "./tmp/Resources/ossitter.service"
sed -i "s,{ch_user},$ch_user,gm" "./tmp/Resources/ossitter.service"


echo "Modify rights on $installFolder recursively"
chmod 744 $fullIF
chmod 644 $fullIF/*
echo "Giving execution to $installFolder/OsSitter.py"
chmod 744 $fullIF/OsSitter.py

echo "Modify ossitter.service"
#pyth_file=$(realpath $installFolder/OsSitter.py)
#echo $pyth_file

echo "Changing owner to root"
chown -R $ch_user: $fullIF


# install as a service
cp ./tmp/Resources/ossitter.service /lib/systemd/system/ossitter.service
chmod 644 /lib/systemd/system/ossitter.service

systemctl daemon-reload
systemctl enable ossitter
echo "daemon installed and enabled, but not started."
systemctl status ossitter
#chmod 644 /lib/systemd/system/ossitter.service

echo "Finished... If this is a fresh installation, you need to configure"
exit