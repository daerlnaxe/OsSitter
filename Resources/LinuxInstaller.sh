#!/bin/bash
# coding: utf-8

# Make me executable by using 'sudo chmod +x LinuxInstaller.sh'
# Then run me by using './LinuxInstaller.sh'
echo "### Welcome to OsSitter installer for version 1.1"
echo "Compatible OsSitter v4/4.1"
echo "Note: The configuration file will not be overwritten"
# stop if error
set -e

while getopts ":f:l:" opt; do
  # Assign
  case $opt in
    f) tar_file="$OPTARG"
    ;;
    l) lang_file="$OPTARG"
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

# Check tar file
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
fi


# Decompress
if [[ ! -d ./tmp ]]
then
	mkdir ./tmp
fi

echo "Decompressing ..."
# --Strip-components=1 remove root
tar -xzf $tar_file -C tmp --strip-components=1



read -p "Enter the installation folder: " installFolder
if [[ -z "$installFolder" ]]; then
    echo "Exit : no folder selected"
	exit 1
fi
installFolder="$installFolder/OsSitter"
echo "You want install to '$installFolder'"
fullIF=$(realpath $installFolder)




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
mkdir -p $fullIF
cd $fullIF || exit 1
cd - > /dev/null

for file in ./tmp/*.py;
do
	echo "--- moving ${file}";
	mv ${file} $fullIF
done

cp $languageFile $fullIF/currentlang.json

# Stop if error
set -e
echo "Modify rights on $installFolder recursively"
chmod 744 $fullIF
chmod 644 $fullIF/*
echo "Giving execution to $installFolder/OsSitter.py"
chmod 744 $fullIF/OsSitter.py

echo "Modify ossitter.service"
#pyth_file=$(realpath $installFolder/OsSitter.py)
#echo $pyth_file
# PrincipeExecStart=/bin/bash -c 'cd /home/ubuntu/project/ && python app.py'
sed -i "s,{InstallFolder},$fullIF,gm" "./tmp/Resources/ossitter.service"

echo "Changing owner to root"

sudo chown root: $fullIF


# install as a service
sudo cp ./tmp/Resources/ossitter.service /lib/systemd/system/ossitter.service
sudo chmod 644 /lib/systemd/system/ossitter.service

sudo systemctl daemon-reload
sudo systemctl enable ossitter
sudo systemctl start ossitter
sudo systemctl status ossitter
#sudo chmod 644 /lib/systemd/system/ossitter.service
