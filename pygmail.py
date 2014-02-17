from BeautifulSoup import BeautifulSoup
import imaplib
import email
from email.parser import HeaderParser
 
class pygmail(object):
    def __init__(self):
        self.IMAP_SERVER='imap.gmail.com'
        self.IMAP_PORT=993
        self.M = None
 
    def login(self, username, password):
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        rc, response = self.M.login(username, password)
        return rc, response
 
    def get_unread_emails(self, folder='Inbox'):
        messages = []
        status, count = self.M.select(folder, readonly=1)
        typ, data = self.M.search(None, '(UNSEEN)')
 
        for num in data[0].split():
            typ, data = self.M.fetch(num, '(RFC822)')
 
            msg = HeaderParser().parsestr(data[0][1])
 
            msg['Body'] = self.__get_message_body__(data[0][1])
            messages.append(msg)
 
        return messages
 
    def __get_message_body__(self, msgData):
        mail = email.message_from_string(msgData)
 
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart' or part.get_content_subtype() != 'plain':
                continue
 
            return BeautifulSoup(part.get_payload()).prettify()
 
    def mark_unread_emails(self, folder='Inbox'):
        status, count = self.M.select(folder, readonly=0)
        typ, data = self.M.search(None, '(UNSEEN)')
        for num in data[0].split():
            self.M.store(num.replace(' ',','),'+FLAGS','\SEEN')
 
    def logout(self):
        self.M.logout()
