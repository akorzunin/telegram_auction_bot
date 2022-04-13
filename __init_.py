#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv('PWD')
print('PWD')
print(PWD)

import sys
sys.path.insert(1, PWD)