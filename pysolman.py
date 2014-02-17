# https://pypi.python.org/pypi/imaplib2/2.28.1
from pygmail import pygmail

class pysolman(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.g = pygmail()
        self.mails = None

    def __get_mails__( self ):
        mails = None
        self.g.login( self.username, self.password )
        mails = self.g.get_unread_emails()
        self.g.mark_unread_emails()
        self.g.logout()
        return mails

    def __get_status_from_body__( self, body ):
        status = None
        start = body.find('Status')
        if start > 0:
            start = start + 8
            end = body.find('\n', start ) - 1
            stat = body[start:end]
            if stat == 'En desarrollo':
                status = 'Desarrollo'
            if stat == 'En Revisi=F3n':
                status = 'Pruebas'
            if stat == 'Importado a producci=F3n':
                status = 'Archivadas'
        return status

    def __get_pi_from_subject__( self, subject ):
        pi = None
        if subject[0:10].isdigit():
            pin = None
            if subject[13:15] == 'HR':
                pin = subject[16:22]
            else:
                pin = subject[24:30]
            if pin.isdigit():
                pi = pin
        return pi

    def check_updates( self ):
        self.mails = self.__get_mails__()

    def get_status( self ):
        status = {}
        for mail in self.mails:
            subject = mail['Subject'].replace( '=?iso-8859-1?Q?', '' )
            if subject[0:10].isdigit():
                solman = subject[0:10]
                stat = self.__get_status_from_body__( mail['body'] )
                if stat:
                    status[ solman ] = stat
        return status

    def get_pi( self ):
        pis = {}
        for mail in self.mails:
            subject = mail['Subject'].replace( '=?iso-8859-1?Q?', '' )
            if subject[0:10].isdigit():
                pi = self.__get_pi_from_subject__( subject )
                if pi:
                    pis[ pi ] = subject
        return pis
