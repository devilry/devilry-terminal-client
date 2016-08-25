DEV = True

if DEV:
    # developement settings

    API_URL = 'http://localhost:8000/api/'
else:
    # production settings

    API_URL = 'https://devilry.ifi.uio.no/api/'
