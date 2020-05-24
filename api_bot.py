import os
import time
import random
from datetime import datetime,timezone,timedelta
from O365 import Account


def get_datetime():
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    local_dt = dt.astimezone(tzutc_8)
    return local_dt


def check_mailbox(account):
    print("check mail box")
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()
    for message in inbox.get_messages():
        print(message)
    print("check mail box done")


def send_notify_email(account, content):
    print("begin send email...")
    m = account.new_message()
    m.to.add(os.environ["NOTIFY_EMAIL"])
    m.subject = 'Testing E5-bot'
    m.body = "This is a test email from github workflow, check it please" + "<br>" + content
    m.send()
    print("send email done...")


def check_onedrive(account):
    print("check onedrive")
    storage = account.storage()
    my_drive = storage.get_default_drive()  # or get_drive('drive-id')
    root_folder = my_drive.get_root_folder()
    onedrive_contents = ""
    for item in root_folder.get_items(limit=25):
        onedrive_contents += str(item) + "<br>"
    print("check onedrive done")
    return onedrive_contents


if __name__ == "__main__":
    sleep_time = random.randint(1, 180)
    print("sleep {} secs...".format(sleep_time))
    time.sleep(sleep_time)

    client_id = os.environ['CONFIG_ID']
    secret = os.environ['CONFIG_SECRET']
    credentials = (client_id, secret)

    scopes = ['basic', 'message_all', 'onedrive_all']
    account = Account(credentials, scopes=scopes)
    if not account.is_authenticated:
        account.authenticate()

    check_mailbox(account)
    content = check_onedrive(account)

    ldt = get_datetime()
    if ldt.hour == 9 and ldt.day == 5:
        content += "and don't forget to pay credit card bill <br>"
        send_notify_email(account, content)
