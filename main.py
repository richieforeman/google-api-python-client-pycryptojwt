__author__ = "Richie Foreman <richie.foreman@gmail.com>"

import httplib2
from apiclient.discovery import build

from PyCryptoSignedJWT import PyCryptoSignedJwtAssertionCredentials

KEY = "privatekey.pem"
SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_ID = "89576170682-1v4a6kh1l382akel7fs89an8q6kna61u.apps.googleusercontent.com"
SERVICE_ACCOUNT = '89576170682-1v4a6kh1l382akel7fs89an8q6kna61u@developer.gserviceaccount.com'

def main():
    key = open(KEY).read()

    credentials = PyCryptoSignedJwtAssertionCredentials(
        SERVICE_ACCOUNT,
        key,
        scope=" ".join(SCOPES),
        prn="richie@richieforeman.com")
    http = httplib2.Http()
    httplib2.debuglevel = True
    http = credentials.authorize(http)

    service = build(serviceName='drive', version='v2', http=http)

    print service.files().list().execute()

if __name__ == "__main__":
    main()