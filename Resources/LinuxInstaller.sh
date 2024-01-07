#!/bin/bash
# coding: utf-8

# Make me executable by using 'sudo chmod +x LinuxInstaller.sh'
# Then run me by using './LinuxInstaller.sh'

read -p "Enter the installation folder: " installFolder
installFolder="$installFolder/OsSitter"
echo "You want to install in '$installFolder'"

#cd $installFolder || exit 1
#cd -

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

echo "Decompressing ..."
mkdir ./tmp
# --Strip-components=1 remove root
tar -xzf OsSitter-Alpha4.tar.gz -C tmp --strip-components=1

echo "Move files to installation folder"

mkdir -p $installFolder
cd $installFolder || exit 1
cd -

for file in ./tmp/*.py;
do
	echo "moving ${file}";
	mv ${file} $installFolder
done

cp $languageFile $installFolder/currentlang.json

echo "Modify rights on $installFolder recursively"
chmod 744 $installFolder
chmod 644 $installFolder/*
echo "Giving execution to $installFolder/OsSitter.py"
chmod 744 $installFolder/OsSitter.py

echo "Modify ossitter.service"
pyth_file=$(realpath $installFolder/OsSitter.py)
echo $pyth_file
sed -i "s,{InstallFolder},$pyth_file,g" "./tmp/Resources/ossitter.service"



echo "Changing owner to root"
sudo chown root: $installFolder


# install as a service
sudo cp ./tmp/Resources/ossitter.service /lib/systemd/system/ossitter.service
sudo chmod 644 /lib/systemd/system/ossitter.service

sudo systemctl start ossitter
#sudo chmod 644 /lib/systemd/system/ossitter.service
