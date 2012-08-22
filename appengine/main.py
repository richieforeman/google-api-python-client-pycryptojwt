import webapp2

KEY = "privatekey.pem"
SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_ID = "89576170682-1v4a6kh1l382akel7fs89an8q6kna61u.apps.googleusercontent.com"
SERVICE_ACCOUNT = '89576170682-1v4a6kh1l382akel7fs89an8q6kna61u@developer.gserviceaccount.com'

from PyCryptoSignedJWT import PyCryptoSignedJwtAssertionCredentials
import httplib2
from apiclient.discovery import build

class IndexHandler(webapp2.RequestHandler):
    def get(self):
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


app = webapp2.WSGIApplication([('/', IndexHandler)],debug=True)