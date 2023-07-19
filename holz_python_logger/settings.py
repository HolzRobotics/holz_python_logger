import os


PROJECT_NAME = os.getenv('PROJECT_NAME', 'UNKNOWN')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
LOGSTASH_HOST = os.getenv('LOGSTASH_HOST')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT', '0'))
ENVIRONMENT = os.getenv('RUN_LEVEL')
