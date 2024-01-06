# OsSitter
 Watch behavior of Operating system

NO GUI ! It's for Core Servers.

It uses a simple json configuration file to add the things you want to watch

# Last version
Alpha 4 : 
- Translation System
- Detect
    - Sigterm (linux)
    - Ctrl+C

# Todo
- Add new features like
    - uptime
    - free mem
    - inodes
    - free space
    - Custom command
    - Securities
- JSon rebuilder


# Features
- Watching services
    - Time between check
    - Send mail if service is:
        - Stopped
        - Restarted
        - Send mails to several CC
- Time between loop
- Time between mails sent
- Send mails to several CCI
- Hot configuration reload
- Send mail to multiple people
- Detect:
    - Linux
        - Ctrl+C
        - Sigterm


# Sample
Service configuration
```JSon
{
    "nom": "kea-dhcp4",
    "typeA": "service",
    "timer":2,
	"delay_alarm":5
}
```

SMTP configuration
```JSon
"smtp":{
    "smtpstring": "smtp-mail.outlook.com",	
	"port": 587,
	"auth": true,
	"login": "yourmail@outlook.fr",
	"app-password": "yourapppass_for_outlook"
},

```

# Changelog
## 06/01/2024
- Moved all language part to a file
- A new module to write text and format it
- Rewriting everything to make it clean