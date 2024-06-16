[_TOC_]
# Config File
## Config File Lambda
> [] : optionnal
> <> : type

```json
{
        "Version": <string>,
        "Parameters":
        {
                "ServerName": <string>,
                "Debug": <bool>,
                "Stop": <bool>,
                "Sleeper": <int>,
                "Mail":
                {
                    "mutemode": <bool>,
                    "sender": <string>>,
                    "smtp":{
                                "smtpstring": <string>,
                                "port": <int>,
                                "auth": <bool>,
                                ["login": <string>,]
                                ["app-password": <string>]
                        },
                        "to":[
                        {
                                "name": <string>,
                                "address": <string>

                        },
                        {
                                "name": <string>,
                                "address": <string>
                        }
                        ],
                        "cc":[
                        {
                                "name": <string>,
                                "address": <string>
                        }
                        ],
                        "cci":[

                        ]

                }
        },

        "Alertes": [
        {
            "nom": <string> ,
            "typeA": "<service|function>",
            ["trigger": "<string>",]
            "timer": <int>,
            "delay_alarm": <int>
        }
    ]
}
```

### Description:
#### Parameters
- Mail
  - mutemode: don't send mail (used to test algorithm)
  - smtp
    - smtpstring: string to connect to your smtp server
        - outlook: smtp-mail.outlook.com
    - auth : use it if you need a password to use a smtp server

#### Alertes
- nom
- typeA : type of the alert
  - `service` : check status of a daemon
  - `function` : integrated functions to help
    - `mem` : Check memory occupation
- trigger: only for `function`
- timer : time before check, in...
- delay_alarm: time before 2 alarms

<br>
<br>

## Config file modifications
### Update 4.11 > 5
- typeA: new type `function` => you can use it with name `mem` to alert about memory occupation
- add `trigger` after `typeA`: used to give a trigger value. Currently used by `mem` function.


### Update 1 > 4.11
- Add `"Version": <string>` before `"Parameters"`
- Add `"mutemode": <bool>,` before `"sender"`