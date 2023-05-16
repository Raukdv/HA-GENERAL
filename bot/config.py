import os
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv.load_dotenv(
    os.path.join(os.path.normpath(os.getcwd()), '.env')
)

DEBUG = True if os.getenv('DEBUG') == 'True' else False

PDB_DEBUG = True if DEBUG and os.getenv('PDB_DEBUG') == 'True' else False

HA_USERNAME = os.getenv('HA_USERNAME', '')

HA_PASSWORD = os.getenv('HA_PASSWORD', '')

HA_AIRTABLE = os.getenv('HA_AIRTABLE', '')

HA_AIRTABLE_KEY = os.getenv('HA_AIRTABLE_KEY', '')

MAX_RETRIES = os.getenv('MAX_RETRIES', 5)

INSTANCES = os.getenv('INSTANCES', 1)

STATUS_PROCESSING = os.getenv('STATUS_PROCESSING', 36)

STATUS_APPROVED = os.getenv('STATUS_APPROVED', 34)

STATUS_DENY = os.getenv('STATUS_DENY', 35)

WORKERS = int(os.getenv('WORKERS', 1))

#New variables
RETRIES = os.getenv('RETRIES', 50)

USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')

USE_CSV = os.getenv('USE_CSV', 'false')