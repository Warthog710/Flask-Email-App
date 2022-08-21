import os
import yagmail

from uuid_extensions import uuid7str
from bs4 import BeautifulSoup
from subprocess import run

class email:
    out_file = 'out.html'
    in_file = 'in.html'
    
    def __init__(self, db):
        self.__db = db
        self.__password = os.getenv('GMAIL_APP_PASSWORD')
        self.__email_from = os.getenv('EMAIL_FROM')
        self.__email_to = os.getenv('EMAIL_TO')

    def send_email(self, html, request):
        try:
            html = self.__parse_email(html, request)

            with yagmail.SMTP(self.__email_from, self.__password) as mail:
                mail.send(self.__email_to, 'Subject', html)
        except Exception as e:
            print(f'Failed to send email: {e}')
        else:
            print('Email sent!')

    #? The steps required to parse an emails HTML to be usable
    def __parse_email(self, html, request):
        html = self.__host_base64_images(html, request)
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

    #? Pulls out base64 images and hosts them on the server
    def __host_base64_images(self, html, request):
        soup = BeautifulSoup(html, 'lxml')

        #? Saving into a pil image
        # image = Image.open(io.BytesIO(base64.b64decode(data)))

        for image in soup.find_all('img'):
            if 'base64' in image['src']:
                header, data = image['src'].split(',', maxsplit=1)
                image_type = header.split(':', maxsplit=1)[1].split(';', maxsplit=1)[0]
                image_id = uuid7str()

                self.__db.save_image(image_id, image_type, data)

                if 'date-filename' in image:
                    del image['data-filename']

                # Replace with URL to image
                image['src'] = request.url_root + f'image/{image_id}'

        return str(soup)
