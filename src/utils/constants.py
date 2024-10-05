import os

GAE_ENV = os.environ.get('GAE_ENV')
IS_LOCAL = (GAE_ENV is None or GAE_ENV == 'localdev')
