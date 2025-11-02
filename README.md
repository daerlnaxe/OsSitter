[TOC]

# OsSitter
## Documentation
- [Development](./Doc/dev.md)
- [Configuration](./Doc/config.md)
- [Help](./Doc/help.md)

## New
Happy to say i successful made Linux installer and uninstaller...
It's now easy to implement. 
It gives possibilities:
- to create a service account, and install in its home folder.
- Give rights
- Install it as a systemd daemon
- Doesn't launch immediatly but enable, to let you configure.
- Almost a generic installer

!!! Warning I don't have a lot of time to develop but this program run under a production environment more than 1 year and is very helpful. I stay in alpha because i have a lot of things to add, and i prefer to warn people juste in case ...

## About
 Watch behavior of Operating system

NO GUI ! It's for Core Servers.

It uses a simple json configuration file to add the things you want to watch
It uses a simple json language file to translate as you wish.


## Last version
[Alpha 5.60](./Doc/dev.md#alpha-5.60)

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
