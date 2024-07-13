Ban de outlook : [page](https://support.microsoft.com/en-us/office/sending-limits-in-outlook-com-279ee200-594c-40f0-9ec8-bb6af7735c2e)
```
Traceback (most recent call last):
  File "/home/supervision/./OsSitter.py", line 482, in <module>
    if not sup.test():
  File "/home/supervision/./OsSitter.py", line 308, in test
    self.mailer.normal_mail("just_a_test")
  File "/home/supervision/MailCreator.py", line 105, in normal_mail
    mails.Send(self.mail_params.sender, subject , message, self.mail_params);
  File "/home/supervision/MailSender.py", line 204, in Send
    mailserver.send_message(msg)
  File "/usr/lib64/python3.9/smtplib.py", line 986, in send_message
    return self.sendmail(from_addr, to_addrs, flatmsg, mail_options,
  File "/usr/lib64/python3.9/smtplib.py", line 908, in sendmail
    raise SMTPDataError(code, resp)
smtplib.SMTPDataError: (554, b'5.2.0 STOREDRV.Submission.Exception:OutboundSpamException; Failed to process message due to a permanent exception with message [BeginDiagnosticData]WASCL UserAction verdict is not None. Actual verdict is RefuseQuota. OutboundSpamException: WASCL UserAction verdict is not None. Actual verdict is RefuseQuota.[EndDiagnosticData] [Hostname=AM9P192MB0935.EURP192.PROD.OUTLOOK.COM]')
```
