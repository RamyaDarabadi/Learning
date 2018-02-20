from scrapy.mail import MailSender

def get_email(source_name):
    mailer = MailSender(mailfrom = "ramyalatha3004@gmail.com",smtphost  = "smtp.gmail.com", smtpport = 587, smtpuser = "ramyalatha3004@gmail.com", smtppass = "R01491a0237")
    mailer.send(to = ["raja@emmela.com"], subject = "Test mail : Report", body = "Run completed for %s " %source_name, cc = ["ramya@emmela.com","ramya@atad.xyz"])
