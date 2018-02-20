import sys
import os
import datetime
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
sys.path.append('../spiders')
from  db import *


class Travelblogs(object):
    def __init__(self):
        self.con, self.cur = get_pymysql_connection()
        self.tables = {"MakeMyTrip":"mmt", }#source_name: table name
        self.get_rec_query = "select count(*) from %s where date(modified_at) = curdate()"

    def main(self):
        try:
                recievers_list = ['ramya@emmela.com', 'raja@emmela.com']
                sender, receivers = 'ramyalatha3004@gmail.com', ','.join(recievers_list)
                msg = MIMEMultipart('alternative')
                msg['Subject'] = 'Travel Blogs Report on %s'%(str(datetime.datetime.now().date()))
                mas = '<h3>Hi,</h3>'
                mas += '<p>Please find the below stats for travel blogs</p>'
		mas += '<table  border="1" cellpadding="0" cellspacing="0" >'
		mas += '<tr><th>Source</th><th>Table Name</th><th> Number of records</th><th>Status</th></tr>'
                for source_name, table_name in self.tables.iteritems():
                        self.cur.execute(self.get_rec_query % table_name)
                        no_of_records = self.cur.fetchone()
                        status = 'Success'
                        if no_of_records:
                            no_of_records = no_of_records[0]
                        else:
                            no_of_records = 0
                        if no_of_records == 0:
                            status = 'Fail'
        		mas += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (source_name, table_name, no_of_records, status)
		mas += '</table>\n\n\n'
                msg['From'] = sender
                msg['To'] = receivers
                tem = MIMEText(''.join(mas), 'html')
                msg.attach(tem)
                s = smtplib.SMTP('smtp.gmail.com:587')
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, 'ramya3004')
                total_mail=(recievers_list)
                s.sendmail(sender, (total_mail), msg.as_string())
                s.quit()
                print 'sucess'
        except Exception as e:
                print e

if __name__ == '__main__':
        Travelblogs().main()

