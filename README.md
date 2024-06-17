[TOC]

# OsSitter
## New
Happy to say i successful made Linux installer and uninstaller...
It's now easy to implement. 
It gives possibilities:
- to create a service account, and install in its home folder.
- Give rights
- Install it as a systemd daemon
- Doesn't launch immediatly but enable, to let you configure.
- Almost a generic installer

!!! Warning I don't think there is people interested for the while but wait next release, i need to verify again and again there is no error. I made a lot of tests, but just in case...

## About
 Watch behavior of Operating system

NO GUI ! It's for Core Servers.

It uses a simple json configuration file to add the things you want to watch
It uses a simple json language file to translate as you wish.


## Last version
[Alpha 5](#alpha-5)


# Todo
- Add new features like
    - [ ] uptime
    - [x] free mem
    - [ ] inodes
    - [ ] free space
    - [ ] Custom command
    - [ ] Securities
- [x] Move mails part
- [ ] Check installer to verify if Ressources folder is correctly moved during installation.
- [ ] improving mail features
	- [ ]  Timestamp
- [ ] See possibilities to send cli message to all users connected on linux.
- [ ] I still standing, yeah, yeah, yeah (daily mail)

<br>


# Features
- Watching services
    - Time between check
    - Send mail if service is:
		- Started
        - Stopped
        - Restarted
    - Time between mails sent
- Functions:
    - Memory test: give % used
- Mails
    - Send mail to multiple people
    - Send mails to several CC
    - Send mails to several CCI
- Configuration
    - Hot configuration reload ('new-config.json')
    - Rebuild in safe mode if config file deleted
    - Time between loop    
- Detect:
	- [CRTL]+[C]
    - Linux
        - SIGTERM
- Tests on init
- Send about its health mail when:
	- Loaded
	- Stopped by [CRTL]+[C]
	- Linux:
		- SIGTERM
		

<br>

# Settings
## Language files
You can make your own language files

Version x.y.z:
- x: Major (me), like new tags or renaming existing tags.
- y: Medium (all), about the translation.
- z: Minor (all), like minor modifications in content.

		
## Configuration
!!! warning Samples certified only for v2 for the while.



<br>

# Changelog
## Alpha 5.1
06/2024
- New feature: "functions"
    - First, memory test with alerting
- BugFix:
	- Hot config loading
 - Improving:
 	- Split for mails part. 

## Alpha 4.1
07/01/2024
- Installer.sh for Linux installation as a service
- Corrections: 
	- Some visual bugs.
- Visual:
	- Show program version
	- Show language version
- Rebuild a json config file at starting, if missing.
- DxHelios: 
    - warning message

## Alpha 4.0
06/01/2024
- Moved all language part to a file
- A new module to write text and format it
- Rewriting everything to make it clean

<br>

# Sums
```

```
