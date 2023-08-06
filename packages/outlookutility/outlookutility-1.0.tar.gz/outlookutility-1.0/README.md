## Outlook Msg Automation functions

#### display_email: Display draft of email
```python
def display_email(message: str, subject: str, to_list: str, cc_list: str):
    """
        :param message: HTML String with Email message contained. See Examples/Email_Strings.py
        :param subject: Subject String
        :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        """
```
##### Example Call
```python
test_html = f"""
    <HTML>
    <BODY>
    Package Testing Email
    <br>
    </BODY>
    </HTML>"""

outlook_msg_automation.display_email(
    test_html,
    "PyPi Test",
    "a@abc.com; b@abc.com;",
    "c@abc.com;",
)
```

#### display_email_with_attachments: Display draft of email with attachments. Can send any number/type of attachments in email. 
```python
def display_email_with_attachments(message: str, subject: str, to_list: str, cc_list: str, *args):
    """
        :param message: HTML String with Email message contained. See Examples/Email_Body.html.
        :param subject: Subject String
        :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param args: Optional attachment arguments, pass as raw file path or stringified file path.
        """
```
##### Example Call
```python
test_html = f"""
    <HTML>
    <BODY>
    Package testing email with attachments
    <br>
    </BODY>
    </HTML>"""

outlook_msg_automation.display_email_with_attachments(
    test_html,
    "PyPi Test",
    "a@abc.com; b@abc.com;",
    "c@abc.com;",
    r"C:\Users\mjens\Github\Outlook_PyPi_Package\tests\test_1.txt",
    r"C:\Users\mjens\Github\Outlook_PyPi_Package\tests\test_2.txt",
)
```

#### email_without_attachment: Send email without attachments. 
```python
def email_without_attachment(message: str, subject: str, to_list: str, cc_list: str):
    """
        :param message: HTML String with Email message contained. See Examples/Email_Strings.py
        :param subject: Subject String
        :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        """
```
##### Example Call
```python
test_html = f"""
    <HTML>
    <BODY>
    Package Testing Email
    <br>
    </BODY>
    </HTML>"""

outlook_msg_automation.email_without_attachment(
    test_html,
    "PyPi Test",
    "a@abc.com; b@abc.com;",
    "c@abc.com;",
)
```

#### email_with_attachments: Send email with attachments. Can send any number/type of attachments in email. 
```python
def email_with_attachments(message: str, subject: str, to_list: str, cc_list: str, *args):
    """
        :param message: HTML String with Email message contained. See Examples/Email_Body.html.
        :param subject: Subject String
        :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param args: Optional attachment arguments, pass as raw file path or stringified file path.
        """
```
##### Example Call
```python
test_html = f"""
    <HTML>
    <BODY>
    Package testing email with attachments
    <br>
    </BODY>
    </HTML>"""

outlook_msg_automation.email_with_attachments(
    test_html,
    "PyPi Test",
    "a@abc.com; b@abc.com;",
    "c@abc.com;",
    r"C:\Users\mjens\Github\Outlook_PyPi_Package\tests\test_1.txt",
    r"C:\Users\mjens\Github\Outlook_PyPi_Package\tests\test_2.txt",
)
```

#### notify_error: Automated email report for use in exception catch. 
```python
def notify_error(report_name, error_log, to_list: str):
    """

    :param to_list: List of emails to receive notification.
    :param report_name: Name of automated report.
    :param error_log: Raised exception or other error to report.
    """
```
##### Example Call
```python
try:
    some_function()
except Exception as e:
    outlook_msg_automation.notify_error(f"{os.path.basename(__file__)}", e, "a@email.com")
```