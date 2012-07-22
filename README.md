google-api-python-client-pycrypto
=============

A third party add-on that allows for signing JWT assertion credentials using PyCrypto.

Author
-------
Richie Foreman <richie.foreman@gmail.com>

Why?
-------
google-api-python-client's SignedJWTAssertionCredentials expects both a PKCS12 key, and an OpenSSL environment.   PyCrypto does not play nicely with PKCS12 certs -- yet. This project ports SignedJWTAssertionCredentials to play nicely with PyCrypto and PEM Keys.

AppEngine
------
AppEngine currently supports PyCrypto version 2.3.  However, Crypto.Signature was added in 2.6.  Hopefully this POC and the potentially surrounding community interest will plead our case for PyCrypto 2.6 support in AppEngine

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
#!/bin/bash
openssl pkcs12 -passin pass:notasecret -in privatekey.p12 -nocerts -passout pass:notasecret -out key.pem
# this next line is kind of odd -- but the key is exported with some metadata at the beginning that PyCrypto can't digest.
tail -n +5 key.pem > privatekey.pem
rm key.pem
```

Console Use
------

```
import httplib2
from apiclient.discovery import build

from AppEngineSignedJWT import PyCryptoSignedJwtAssertionCredentials

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
