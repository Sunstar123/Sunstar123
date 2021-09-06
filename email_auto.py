import imaplib
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = 'spzengo@gmail.com'
password = None # sorry cant go giving this away
imap_url = 'imap.gmail.com'
receiver = None # also this

date_to_date = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
                11: "Nov", 12: "Dec"}


def new_message_check(date):
    try:
        bob = datetime.datetime.now()
        bobb = str(bob).split("-")
        bobb[2] = bobb[2][0:2]
        jefff = date.split(" ")
        bobb.reverse()
        if int(bobb[0]) == int(jefff[0]) and int(bobb[2]) == int(jefff[2]) and date_to_date[int(bobb[1])] == jefff[1]:
            # print("date match")
            return True
        else:
            # print("date not match")
            return False
    except ValueError:
        # print("error")
        pass


def create_message(receiver, sender, header, body):
    msg = MIMEMultipart()
    msg['To'] = receiver
    msg['From'] = sender
    msg['Subject'] = header
    msg.attach(MIMEText(body, 'plain'))

    message = msg.as_string()  # MIME makes msg a string that conforms to gmail's standards

    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.login(sender, password)  # log in to the server with username and password
    server_ssl.sendmail(sender, receiver, message)
    server_ssl.quit()
    # print(message)
    # print(f"message sent from {receiver} to {sender}")


# Function to get email content part i.e its body part
def get_body(message):
    if message.is_multipart():
        return get_body(message.get_payload(0))
    else:
        return message.get_payload(None, True)

    # Function to search for a key value pair


def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


# Function to get the list of emails under this label
def get_emails(result_bytes, con):
    msgs = []  # all the email data are pushed inside an array
    iters = 0
    for num in reversed(result_bytes[0].split()):
        if iters < 15:
            typ, data = con.fetch(num, '(RFC822)')
            msgs.append(data)
        iters += 1
    return msgs


def main():
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(username, password)
    con.select('Dad')
    msgs = get_emails(search('FROM', receiver, con), con)

    # print("Starting Parsing")
    hi = []
    for msg in msgs[::-1]:
        for sent in msg:
            if type(sent) is tuple:
                # encoding set as utf-8
                content = str(sent[1], 'utf-8')
                data = str(content)
                try:
                    indexstart = data.find("MIME-Version: 1.0")
                    indexstart += 14
                    data2 = data[indexstart + 5: len(data)]
                    indexend = data2.find("quoted-printable")
                    indexend += 16

                    hi.append(data2[0: indexend])

                except UnicodeEncodeError:
                    pass

    for message in hi:
        indexs = message.find("Date")
        indexe = message.find("Message-ID")
        dat = message[indexs+11:indexe-17]
        if new_message_check(dat):
            indexs = message.find('charset="UTF-8"') + 19
            indexe = message.find('Content-Type: text/html') - 35
            body = message[indexs: indexe]
            indexs = message.find('Subject: ') + 9
            indexe = message.find('To: ') - 2
            header = message[indexs: indexe]
            create_message(receiver, username, header, body)


if __name__ == "__main__":
    main()
