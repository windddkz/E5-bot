from O365 import Account


def check_mailbox(account):
    print("check mail box")
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()
    for message in inbox.get_messages():
        print(message)
    print("check mail box done")


def check_onedrive(account):
    print("check onedrive")
    storage = account.storage()  # here we get the storage instance that handles all the storage options.
    drives = storage.get_drives()
    print(drives)
    my_drive = storage.get_default_drive()  # or get_drive('drive-id')
    root_folder = my_drive.get_root_folder()
    for item in root_folder.get_items(limit=25):
        print(item)
        if item.is_folder:
            print(item.get_items(2))  # print the first to element on this folder.
        elif item.is_file:
            if item.is_photo:
                print(item.camera_model)  # print some metadata of this photo
            elif item.is_image:
                print(item.dimensions)  # print the image dimensions
            else:
                # regular file:
                print(item.mime_type)
    print("check onedrive done")


if __name__ == "__main__":


    credentials = (client_id, secret)

    scopes = ['basic', 'message_all', 'onedrive_all']
    account = Account(credentials, scopes=scopes)
    if not account.is_authenticated:
        account.authenticate()

    check_mailbox(account)
    check_onedrive(account)
