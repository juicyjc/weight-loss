API_PROTOCOL = 'http'
API_CONTAINER = 'weightloss-api'
API_PORT = 5000

# Urls
URL_APPS = '{}://{}:{}/apps/'.format(API_PROTOCOL, API_CONTAINER, API_PORT)
URL_ACCESS = '{}://{}:{}/apps/access/'.format(API_PROTOCOL, API_CONTAINER, API_PORT)
URL_ACCESS_TOKEN = '{}://{}:{}/apps/access_token/'.format(API_PROTOCOL, API_CONTAINER, API_PORT)
URL_ENTRIES = '{}://{}:{}/entries/'.format(API_PROTOCOL, API_CONTAINER, API_PORT)

