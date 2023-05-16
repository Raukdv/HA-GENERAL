import json
import csv
import binascii
import os
from datetime import datetime
import requests

from selenium.webdriver.common.by import By

from ..base.selenium import BaseSelenium
from .. import config


class PorchSelenium(BaseSelenium):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.csv_file = None
        self.status = None #Data normal ejemplo, Ok, error_500 etc
        self.last_loop_n_retries = 0 # Numero de retries en el loop, por defecto es 5
        self.last_loop_retries_count = 0 # Contador de retries en el loop
        self.retries = int(config.RETRIES) #Per default retries -> 50 times
        self.user_agent = config.USER_AGENT #Default user agent for requests
        self.use_csv = False if config.USE_CSV == 'false' else True #Bool for create and use CSV or not

    def __call__(self):
        try:
            return self.handle()
        except Exception as err:
            print(err)
            self._wait(5)
        finally:
            print("Work Done, Closing bot")
            self.quit_driver()

    def handle(self):
        self.driver = self.get_driver(size=(1200, 700))
        self.do_login()
        self.go_to_oportunities()
        links = self.get_list_items()

        #Create CSV for use as dump data (Airtable)
        if self.use_csv:
            self.create_csv_file()

        for link in links:
            content = self.get_link_data(link)
            if content:
                #print("content valid for shipment")
                self.send_to_airtable(content)
            else:
                print('The next link will be skipped: {}'.format(link))
            
            del content

        self._wait(5)
    
    #CSV File creator
    def create_csv_file(self):
        title = 'archivo/csv/EasyLink-'+binascii.hexlify(os.urandom(3)).decode()+'-T'+datetime.now().strftime('%H-%M-%S')
        csv_file = open(f'{title}.csv', mode='w', newline='')
        #File Map
        fieldnames = [
            'postApprovalConsumerName',
            'conAddressLine1',
            'conAddressLine2',
            'consumerCity',
            'consumerState',
            'consumerZip',
            'consumerDayTimePhone',
            'consumerEveningPhone',
            'consumerCellPhone',
            'taskDescription',
            'srComments',
            'token',
            'preciseLatitude',
            'preciseLongitude',
            'submitDateTime'
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        self.csv_file = writer

    def do_login(self):
        self.driver.get('https://pro.homeadvisor.com/login?execution=e1s1')
        self.fill_input(By.ID, 'username', config.HA_USERNAME)
        self.fill_input(By.ID, 'password', config.HA_PASSWORD)
        self.click_element(By.CSS_SELECTOR, 'input[type="submit"]')

    def go_to_oportunities(self):
        self.driver.get('https://pro.homeadvisor.com/opportunities/')
        self._wait(5)

    def get_list_items(self):
        elements = []
        response = []

        while len(elements) == 0:
            elements = self.get_elements(
                By.CSS_SELECTOR, '.lead-card-link'
            )

        for element in elements:
            link = element.get_attribute('href')
            link = link.replace('/opportunities/details/OL/', '/ols/lead/')
            if not link.startswith('http'):
                link = f'https://pro.homeadvisor.com{link}'
            response.append(link)
        
        return response

    def get_link_data(self, link):
        self.driver.get(link)

        #Check if expired
        try:
            expired = self.get_element(By.CSS_SELECTOR, '.spOpportunityHeader__title')
        except:
            expired = None

        if expired and expired.text.lower() == 'opportunity expired':
            value = None
            print('The next link is expired: {}'.format(link))
        else:
            content = self.get_element(By.ID, 'jsonModel')
            content = content.get_attribute('innerHTML')
            value = content
            print('The next link is avaliable: {}'.format(link))

        return value 

    def parse_content(self, content):
        if content.startswith('"'):
            content = content[1:-1]
        content = json.loads(content)

        fields = [
            'postApprovalConsumerName',
            'conAddressLine1',
            'conAddressLine2',
            'consumerCity',
            'consumerState',
            'consumerZip',
            'consumerDayTimePhone',
            'consumerEveningPhone',
            'consumerCellPhone',
            'taskDescription',
            'srComments',
            'token',
            'preciseLatitude',
            'preciseLongitude',
        ]
        response = {}

        for field in fields:
            try:
                response[field] = content[field]
            except KeyError:
                continue

        response['submitDateTime'] = (
            '{year:04}-{month:02}-{day:02}T{hour:02}:{minute:02}:{second:02}.000Z'
        ).format(
            year=content['submitDateTime']['year'],
            month=content['submitDateTime']['monthValue'],
            day=content['submitDateTime']['dayOfMonth'],
            hour=content['submitDateTime']['hour'],
            minute=content['submitDateTime']['minute'],
            second=content['submitDateTime']['second'],
        )

        return response
    
    #CSV Writer
    def send_to_csv(self, content):
        print("The content will be write in csv file")
        self.csv_file.writerow(content)

    def send_to_airtable(self, content):
        content = self.parse_content(content)
        #Use in here for more confortable access
        if self.use_csv:
            self.send_to_csv(content)

        #Ini the rest of the code
        url = config.HA_AIRTABLE
        content = dict(records=[dict(fields=content)])

        #Retries
        for retry_loop_connection in range(1,int(self.retries)+(int(1))):
            self.last_loop_retries_count = retry_loop_connection 
            print ("Start retry # " + str(retry_loop_connection)+' / '+str(self.retries))
        
            response = requests.post(
                url, 
                json=content, 
                headers={
                'User-Agent': self.user_agent,
                'Authorization': f'Bearer {config.HA_AIRTABLE_KEY}'
                }
            )

            #Condicional status - Anything that goes between 200 and 300 will be taken as completed else will be be reattempted.
            if response.status_code >= 200 and response.status_code < 300:
                self.status = "OK"
                print("One lead sended to airtable with HTTP status: "+str(response.status_code))
                return True
            else:
                self.status = "Error - "+str(response.status_code)
                print("Some issue found with HTTP status: "+str(response.status_code))
        #import pdb
        #pdb.set_trace()