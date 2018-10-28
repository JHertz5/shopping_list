'''
module to send an email to jukka.hertzog@live.co.uk through shoppinglist44@gmail.com
written for automated shopping list project
'''

import smtplib
import encrypt

def getEmailAddresses():
    '''
    read email addresses from txt file
    '''
    file = open('email_addresses.txt','r')
    return [ x.rstrip() for x in file.readlines() ] # rstrip to remove trailing whitespace

def sendEmail(subject,body):
    '''
    sends email to jukka.hertz@live.co.uk through shoppinglist44@gmail.co.uk
    subject - string, will be subject of email
    body - string, will be body of email
    '''
    smtpObject = smtplib.SMTP('smtp.gmail.com',587) # connect to smtp server
    smtpObject.ehlo() # get acknowledgement from server
    smtpObject.starttls() # start ttls encryption

    (fromAddress,toAddress) = getEmailAddresses() # get email addresses
    password = encrypt.loadAndDecryptString() # get password
    smtpObject.login(fromAddress,password) # login to account
    result = smtpObject.sendmail(fromAddress,toAddress,\
                                 'Subject: ' + subject + '\n' + body)
    if result != {}:
        print(result) # if return of sendmail() is not empty dict, send mail failed

    smtpObject.quit()

if __name__ == '__main__':
    sendEmail('Can you hear me?','ayy lmao')
    print('email sent')
