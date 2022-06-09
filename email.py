import os
from os import stat
from smtplib import SMTP_SSL
from ssl import create_default_context



def send_email(email_address, email_pass, email_server, email_port, message):
    with SMTP_SSL(email_server, email_port, context=create_default_context()) as smtp:
        smtp.connect(email_server, email_port)
        smtp.login(email_address, email_pass)
        smtp.sendmail(email_address, email_address, message)


# file access:
file = "/home/user/attacked_file.txt"
file_last_access_time = stat(file).st_atime
file_last_permissions = stat(file).st_mode
file_moved = False

# email:
email_address = 'myemail@gmail.com'
email_pass = 'mypassword'
email_server = 'smtp.gmail.com'
email_port = 465


while True:
    if os.path.exists(file):
        try:
            file_stats = stat(file)
            if (file_last_access_time != file_stats.st_atime or
                file_last_permissions != file_stats.st_mode):
                file_last_access_time = file_stats.st_atime
                file_last_permissions = file_stats.st_mode
                send_email(email_address, email_pass, email_server, email_port, "file was accessed!")
                print(f"file was accessed: {file_last_access_time}, sending email...")
                file_moved = False
        except:
            file_last_access_time = file_stats.st_atime
            file_last_permissions = file_stats.st_mode
            send_email(email_address, email_pass, email_server, email_port, "file was accessed!")
            print(f"file was tempered with: {file_last_access_time}, sending email...")
            file_moved = False

    else:
        if not file_moved:
            send_email(email_address, email_pass, email_server, email_port, "file was moved!")
            print("file was moved, sending email...")
            file_moved = True