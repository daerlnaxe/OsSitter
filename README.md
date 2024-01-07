[TOC]

# OsSitter
## About
 Watch behavior of Operating system

NO GUI ! It's for Core Servers.

It uses a simple json configuration file to add the things you want to watch
It uses a simple json language file to translate as you wish


## Last version
[Alpha 4.1](#alpha-41)


# Todo
- Add new features like
    - [ ] uptime
    - [ ] free mem
    - [ ] inodes
    - [ ] free space
    - [ ] Custom command
    - [ ] Securities
- Move mails part

<br>


# Features
- Watching services
    - Time between check
    - Send mail if service is:
		- Started
        - Stopped
        - Restarted
    - Time between mails sent
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

### Service configuration
```JSon
{
    "nom": "kea-dhcp4",
    "typeA": "service",
    "timer":2,
	"delay_alarm":5
}
```

### SMTP configuration
```JSon
"smtp":{
    "smtpstring": "smtp-mail.outlook.com",	
	"port": 587,
	"auth": true,
	"login": "yourmail@outlook.fr",
	"app-password": "yourapppass_for_outlook"
},

```

<br>

# Changelog
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
59865762076c311eedbbc2d3f06139061491e13d5771d32fb104c9b6f0c8a480 *AlertClass.py
5eb1fba5df1c4ded192dabaab0fa71b0f95c7186ae1f969c371b9df309e17eae *Check_Service.py
fe96c8584e547d839d6429f79f980dacbc416178b005c67774bc2af027032fd9 *Config.py
97ea65eb92e2409e0beec95cd04812feae71ff196c8def69e969197ba27fdbed *DxHelios.py
bed69206fccc7b84f3e21878cef34aa77c4e7aff008bac672a9c454dd97ad37a *OsSitter.py
07c7d4f0962c775c6069dde071c5d025d708db4ab9bb111afc8ddd228bb4448f *SendMail.py
```