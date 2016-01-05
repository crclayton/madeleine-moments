# notes-flashback

# This program sends an email to me once a day containing a
# page from my old notes. It creates a flashback, reminding
# me of a lecture/concept that I might have forgotten about
# without the review. Alternatively, if I look at the notes
# and have no recollection of them, it'll signal to me that
# I need to review a topic.

# To use: create a task scheduler event to call the following: 
# > python notes_flashback.py <your email> <your password> <your notes pdf>

# 03-Jan-16



from PyPDF2 import PdfFileReader, PdfFileWriter
from random import randint

import smtplib, sys
import email.mime.multipart as multipart, email.mime.application as application


def get_random_pdf_page(input_pdf_path, output_pdf_path):
    pdf_file = PdfFileReader(input_pdf_path)

    random_page_number = randint(1, pdf_file.getNumPages() - 1)
    random_pdf_page = pdf_file.getPage(random_page_number) 

    page_to_email = PdfFileWriter()
    page_to_email.addPage(random_pdf_page)

    file_to_email = open(output_pdf_path,"wb")
    page_to_email.write(file_to_email)
    file_to_email.close()

def create_pdf_attachment(filename):
    file = open(filename, "rb")
    attachment = application.MIMEApplication(file.read(),_subtype="pdf")
    file.close()
    attachment.add_header("Content-Disposition", "attachement", filename=filename)
    return attachment

def send_gmail(recipient, sender, password, attachment):

    mail = multipart.MIMEMultipart()
    mail["Subject"] = "Notes Flashback"
    mail["From"] = sender
    mail["To"] = recipient
    mail.attach( create_pdf_attachment(attachment) )

    server = smtplib.SMTP('smtp.live.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender,[recipient], mail.as_string())
    server.close()
 
def main(email, password, pdf):
    print("opening pdf")
    get_random_pdf_page(pdf, "temp.pdf")

    print("sending email")
    send_gmail(email, email, password, "temp.pdf")

    print("email sent")

if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1], sys.argv[2], sys.argv[3])