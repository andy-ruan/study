#!/usr/local/bin/python
#encoding:GBK
import os
import sys
from email.Header import Header 
from email.MIMEText import MIMEText 
from email.MIMEMultipart import MIMEMultipart 
import smtplib, datetime 


def sendmail(mail_from, mail_to, mail_subject, mail_file, mail_attachments):
    msg = MIMEMultipart() 

    att = MIMEText(open(mail_file , 'rb').read(), 'base64', 'gb2312') 
    att["Content-Type"] = 'text/html; charset=GBK2312' 
    msg.attach(att) 
    
    attachments_list = mail_attachments.split(';')
    for fname in attachments_list:
        if not os.path.isfile(fname):
            continue
        att = MIMEText(open(fname, 'rb').read(), 'base64', 'gb2312') 
        att["Content-Type"] = 'application/octet-stream' 
        att["Content-Disposition"] = "attachment; filename=" + str(fname)
        msg.attach(att) 
    #$smtp = Net::SMTP->new('172.25.7.178');
    #$smtp->auth('bjsearch','TSHP123!@#abc') or die "authertication failed: $!\n";
    #$smtp->mail('bjsearch@tencent.com');
    mail_from = 'bjsearch@tencent.com'
    msg['subject'] = Header(mail_subject, 'gb2312') 
    msg['from'] = mail_from
    msg['to'] = mail_to
    msg['subject'] = Header(mail_subject, 'gb2312') 
    server = smtplib.SMTP('172.25.7.178')
    assert server.login('bjsearch', 'TSHP123!@#abc')
    server.sendmail(mail_from, mail_to.split(';'), msg.as_string()) 
    server.close 

if __name__ == "__main__":
    sendmail(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
