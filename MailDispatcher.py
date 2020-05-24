import email
import imaplib
import time
from SubjectHandler import SubjectHandler

SubHandler = SubjectHandler()

mail_addr = None
mail_pwd = None

"""
CONFIG SECTION
"""
imap_port = 993
imap_server = "imap.gmail.com"
mail_domain = "gmail.com"
mail_time_delta = 30  # in seconds

secrets_file = "./secrets.txt"

# add all nodes here in this(↓) pattern
# SubHandler += SubjectHandler.Node(regex, function)
SubHandler += SubjectHandler.Node("Test[0-9]*", lambda x: print(str(x)))

"""
END OF CONFIG SECTION
"""


def import_secrets(file):
    """
    will save the secrets like mail address and password to variables, so they aren't hardcoded
    :param file: path to file: content is '[MAIL]\n[PWD]'
    :return: secrets, that can be saved to global variables
    """
    global mail_addr
    global mail_pwd
    with open(file) as f:
        mail_addr = f.readline()
        mail_pwd = f.readline()
    if '@' not in mail_addr:
        mail_addr += '@' + mail_domain


def mail_handling():
    """
    Opens inbox, checks for new email fetches then and deletes them from the inbox
    :return: array of emails: subject, sender, body
    """
    messages = []
    mail_connection = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail_connection.login(mail_addr, mail_pwd)
    mail_connection.select('inbox')

    typ, data = mail_connection.search(None, 'ALL')
    mail_ids = data[0].split()
    for i in reversed(mail_ids):
        mail_connection.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                email_content = str(msg)
                messages.extend([email_subject, email_from, email_content])
        mail_connection.store(i, '\\Deleted')
    mail_connection.logout()
    return messages


import_secrets(secrets_file)
while True:
    SubHandler.run(mail_handling())
    time.sleep(mail_time_delta)





