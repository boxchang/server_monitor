import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from_address = "erp@mail.bbiclark.com"
to_address = "box_chang@mail.bbiclark.com"
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Test email"
msg['From'] = from_address
msg['To'] = to_address
# Create the message (HTML).
html = """\
We are sending an email using Python and Gmail, how fun! We can fill this with html, and gmail supports a decent range of css style attributes too - https://developers.google.com/gmail/design/css#example.
"""
# Record the MIME type - text/html.
part1 = MIMEText(html, 'html')
# Attach parts into message container
msg.attach(part1)
# Credentials
username = 'erp@mail.bbiclark.com'
password = 'P@ssw0rd'
# Sending the email
## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#server.starttls()
#server.ehlo()
server.login(username,password)
server.sendmail(from_address, to_address, msg.as_string())
server.quit()