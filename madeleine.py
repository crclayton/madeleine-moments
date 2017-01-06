from PyPDF2 import PdfFileReader, PdfFileWriter
from random import randint

import smtplib, sys, argparse, os, random
import email.mime.multipart as multipart, email.mime.application as application

parser = argparse.ArgumentParser()
parser.add_argument("email")
parser.add_argument("password")
parser.add_argument("dir")


def get_random_file(dir, type):
    files = [os.path.join(path, filename)
         for path, dirs, files in os.walk(dir)
         for filename in files
         if filename.endswith(type)]

    return random.choice(files)


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


def send_email(recipient, sender, password, attachment="", host="smtp.gmail.com"):
    mail = multipart.MIMEMultipart()
    mail["Subject"] = "Remember this?"
    mail["From"] = sender
    mail["To"] = recipient
    if attachment != "": mail.attach(create_pdf_attachment(attachment))

    server = smtplib.SMTP(host, 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender,[recipient], mail.as_string())
    server.quit()


if __name__ == "__main__":
    arguments = parser.parse_args()

    print("selecting random pdf")	
    pdf = get_random_file(arguments.dir, ".pdf")

    print("selecting random page")
    temp_pdf = os.getcwd() + "/temp.pdf"
    print(temp_pdf)

    get_random_pdf_page(pdf, temp_pdf)

    print("sending email")
    send_email(arguments.email, arguments.email, arguments.password, temp_pdf)

    print("email sent")
