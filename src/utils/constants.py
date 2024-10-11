import os

SECRET_ID = 'client-config'

GAE_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
GAE_ENV = os.environ.get('GAE_ENV')
IS_LOCAL = (GAE_ENV is None or GAE_ENV == 'localdev')
LOCAL_DEV = os.environ.get('LOCAL_DEV', None)
