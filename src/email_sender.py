import smtplib

class EmailSender:
    def __init__(self, provider='gmail'):
        self.host = f"smtp.{provider}.com"
        self.port = 587
    
    def start(self):
        self.server = smtplib.SMTP(self.host, self.port)
        self.server.starttls()
    
    def login(self, username, password):
        self.username = username
        self.password = password
        self.server.login(self.username, self.password)

    def send_mail(self, sender, receiver, message):
        self.server.sendmail(sender, receiver, message)
    
    def exit(self):
        self.server.quit()