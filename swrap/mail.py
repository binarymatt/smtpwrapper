import smtplib
from email.mime.text import MIMEText
def send_mail(msg, connection):
    connection.send_message(msg)

class Message(object):
    def __init__(self, from_address, to, subject, content=None):
        self.from_address = from_address
        if to:
            self.to = list(to)
        else:
            self.to = []
        self.subject = subject
        self.body = content
        self.headers = {}
        self._attachments = []
        self.encoding = 'utf-8'
        
    def _set_attachments(self, attachments=[]):
        self._attachments = attachments
    
    def _get_attachments(self):
        return self._attachments
    
    attachments = property(_get_attachments, _set_attachments)
    def message(self):
        msg = MIMEText(self.body)
        msg['Subject'] = self.subject
        msg['From'] = self.from_address
        msg['To'] = ', '.join(self.to)
        for name, value in self.headers.items():
            name = name.lower()
            msg[name] = value
        return msg

class Connection(object):
    def __init__(self, host, port=25, silent=False):
        self.host = host
        self.port = port
        self.silent = silent
        self.connection = None
    
    def open(self):
        if not self.connection:
            self.connection = smtplib.SMTP(self.host, self.port)
    
    def close(self):
        try:
            self.connection.quit()
        except:
            if self.silent:
                return
            raise
        finally:
            self.connection = None
    
    def send_message(self, message, close_connection=True):
        self.open()
        try:
            self.connection.sendmail(message.from_address, 
                    message.to, 
                    message.message().as_string())
        except:
            if not self.silent:
                raise
            if close_connection:
                self.close()
            return False
        if close_connection:
            self.close()
        return True
            
    
    def send_messages(self, messages, number=0):
        self.open()
        i = 0
        for message in messages:
            if number and i % number == 0:
                try:
                    self.close()
                    self.open()
                except:
                    pass
            self.send_message(message, False)
        self.close()