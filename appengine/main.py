import webapp2

KEY = "privatekey.pem"
SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_ID = "497989677686.apps.googleusercontent.com"
SERVICE_ACCOUNT = '497989677686@developer.gserviceaccount.com'

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
        httplib2.debuglevel = 4
        http = credentials.authorize(http)

        service = build(serviceName='drive', version='v2', http=http)

        docs = service.files().list().execute()
        self.response.out.write("<pre>")
        self.response.out.write("<h1>My Files...</h1>")
        for doc in docs["items"]:
            self.response.out.write("\t" + doc["title"] + "\n")


app = webapp2.WSGIApplication([('/', IndexHandler)],debug=True)