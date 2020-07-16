import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendmail(reciever, otp):  
  sender_email = 'enter sender mail address'
  receiver_email = reciever
  # password = input("Type your password and press enter:")
  password = 'enter your password here'

  message = MIMEMultipart("alternative")
  message["Subject"] = "multipart test"
  message["From"] = sender_email
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message
  text = """\
  Hi,
  How are you?
  This is a test email sent from pyhon!"""
  html = """\
  <html>
    <body>
      <p>Hi there!<br>
        Your OTP for the login system is {}.
      </p>
    </body>
  </html>
  """.format(otp)

  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )