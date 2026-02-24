import os
import certifi
import httplib2
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google_auth_httplib2 import AuthorizedHttp

# ✅ FORCE CERT PATH
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1PTQBIW4wGSy5UsbPt5FxFEyfW_Vl3uyUdHiVcwQbPfE"

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

http = httplib2.Http(ca_certs=certifi.where(), disable_ssl_certificate_validation=True)
authed_http = AuthorizedHttp(creds, http=http)

service = build("sheets", "v4", http=authed_http)


def get_sheet():
    return service.spreadsheets()
