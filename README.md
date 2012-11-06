google-api-python-client-pycrypto
=============

A third party add-on that allows for signing JWT assertion credentials using PyCrypto.

Author
-------
Richie Foreman <richie.foreman@gmail.com>

Why?
-------
google-api-python-client's SignedJWTAssertionCredentials expects both a PKCS12 key, and an OpenSSL environment.   PyCrypto does not play nicely with PKCS12 certs -- yet. This project ports SignedJWTAssertionCredentials to play nicely with PyCrypto and PEM Keys.

oauth2client merging
-------
I hope this code can merge into oauth2client.  oauth2client.crypt currently expects openssl, but there's a fair amount of overlap on some simple methods (base64 encoding, etc).  There's an acknowledged feature request here: http://code.google.com/p/google-api-python-client/issues/detail?id=184

AppEngine
------
View a sample using the Drive V2 API here: https://pycrypt.appspot.com/

Requirements
------
* PyCrypto >= 2.6
* AppEngine SDK >= 1.7.3

Preliminary Setup
------

* Go to Google's API Console and add a new 'service account' api access id -- Be sure to download your private key.
* Take note of your Client ID, Client Secret, and Service Account email address
* In the Google Apps control panel go to Advanced Tools > Manage OAuth Clients.
* Enter the Client ID, and one or more scopes -- Be sure these scopes are also switched on in your Google API Console

Key Conversion
------

We need to convert our PKCS12 cert into a PEM private key

```
openssl pkcs12 -passin pass:notasecret -in privatekey.p12 -nocerts -passout pass:notasecret -out key.pem
openssl pkcs8 -nocrypt -in key.pem -passin pass:notasecret -topk8 -out privatekey.pem
rm key.pem
```

Console Use
------

```
import httplib2
from apiclient.discovery import build

from PyCryptoSignedJWT import PyCryptoSignedJwtAssertionCredentials

KEY = "privatekey.pem"
SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_ID = "****"
SERVICE_ACCOUNT = '****'

def main():
    key = open(KEY).read()

    credentials = PyCryptoSignedJwtAssertionCredentials(
        SERVICE_ACCOUNT,
        key,
        scope=" ".join(SCOPES),
        prn="richard@richieforeman.com")
    http = httplib2.Http()
    httplib2.debuglevel = True
    http = credentials.authorize(http)

    service = build(serviceName='drive', version='v2', http=http)

    print service.files().list().execute()

if __name__ == "__main__":
    main()
```
