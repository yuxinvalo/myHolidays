"""Ask holidays
Usage:
    myholidays_sample [-a] <pretext>
    myholidays_sample [-g] <number> <time>
    myholidays_sample -l

Options:
    -h,--help                       show help list
    -a,--add                        add a good pretext to ask your holidays
    -g,--generate                   generate a mail and send to secretariat
    -l,--show                       show list of your great pretexts

Example:
    python3 myholidays_sample.py -a "J'ai mal au ventre"
    python3 myholidays_sample.py -g 1 "aujourd'hui le cours du matin"
"""

import smtplib
from docopt import docopt
from client import mydict

count = len(open(mydict['path'],'rU').readlines())

def handlepretexts(mode, text):
    if mode == 'r':
        with open(mydict['path'], mode) as fb:
            print(fb.read())
            fb.close()
    elif mode == 'a':
        with open(mydict['path'], mode) as fb:
            fb.write(str(count + 1)+'.')
            fb.write(text)
            fb.write('\n')
            fb.close()
        handlepretexts('r','')
    elif mode == 'g':
        with open(mydict['path'], 'r') as fb:
            for line in fb.readlines():
                if text in line[:2]:
                    return line[3:]
            fb.close()


def sendemail(from_addr, to_addr_list,
              subject, message, time,
              smtpserver='smtp.gmail.com:587'):
    header = 'Subject: %s\n\n' % subject
    msg_final = header + "Bonjour Madame: \n    " + message + "    Je voudrais demander une congé pour " + time +". \n Cordialement \nYuxin SHI"

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(mydict['login'], mydict['pwd'])
    problems = server.sendmail(from_addr, to_addr_list, msg_final.encode('utf-8'))
    server.quit()
    print("I beg to dream and differ from the hollow lies.\nThis is the dawning of the rest of our lives.")
    print("**Edited by Tearsyu**")

if __name__ == '__main__':
    arguments = docopt(__doc__, version='myholidays 0.0.1')
    #print(arguments)
    add = arguments.get('--add')
    gen = arguments.get('--generate')
    ls = arguments.get('--show')

    #Opt manage
    if ls:
        handlepretexts('r', '')

    if add:
        handlepretexts('a',arguments['<pretext>'])

    if gen:
        text = handlepretexts('g',arguments['<number>'])
        print("you choice pretext : %s" %text)
        subject = mydict['subject']
        sendemail(mydict['frommail'], mydict['secretariat'], subject, text, arguments['<time>'] )

    #print(mydict)
