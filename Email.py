import os
import yagmail

from dotenv import load_dotenv
from subprocess import run

class email:
    out_file = 'out.html'
    in_file = 'in.html'
    
    def __init__(self):
        load_dotenv()
        self.__password = os.getenv('GMAIL_APP_PASSWORD')
        self.__email_from = os.getenv('EMAIL_FROM')
        self.__email_to = os.getenv('EMAIL_TO')

    def send_email(self, html):
        try:
            html = self.__parse_email(html)

            with yagmail.SMTP(self.__email_from, self.__password) as mail:
                mail.send(self.__email_to, 'Subject', html)
        except Exception as e:
            print(f'Failed to send email: {e}')
        else:
            print('Email sent!')

    #? The steps required to parse an emails HTML to be usable
    def __parse_email(self, html):
        return self.__bootstrap_email(html)

    #? Calls bootstrap-email CLI to produce syntactical html to send
    def __bootstrap_email(self, html):
        # Output html into a file
        with open(self.in_file, 'w') as file:
            file.write(html)

        args = ['bootstrap-email', f'{self.in_file}', '>', f'{self.out_file}']
        run(args, shell=True) #? Bad practice I know. :(

        # Read created file
        with open(self.out_file, 'r') as file:
            html = file.read()

        # Delete created files
        os.remove(self.in_file)
        os.remove(self.out_file)

        # Remove all \n
        return html.replace('\n', '')
