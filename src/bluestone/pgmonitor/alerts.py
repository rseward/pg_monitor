
import smtplib, email, email.encoders
from email.mime.text import MIMEText

class EmailAlertManager(object):
    """Manages sending email alerts for application events."""

    def __init__(self, smtphost, addresslist, fromAddr):
        """Initialize the manager with a list of email address to notify when an alert occurs."""

        self.addresslist = addresslist
        self.fromAddr = fromAddr
        self.smtphost = smtphost
        

    def alert(self, subject, msg):

        emailMsg = MIMEText( msg )
        emailMsg['Subject'] = subject
        emailMsg['From'] = self.fromAddr
        emailMsg['To'] = ", ".join( self.addresslist )
            
        s = smtplib.SMTP( self.smtphost )
        s.set_debuglevel(True)
        s.sendmail( self.fromAddr, self.addresslist, emailMsg.as_string() )
        s.quit()
        
