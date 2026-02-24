import os
import json
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

# Load service account from environment for deployment (e.g. Vercel)
service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
if not service_account_json:
    raise RuntimeError(
        "GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set. "
        "Configure it in your deployment environment with the service account JSON."
    )

service_account_info = json.loads(service_account_json)

creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES,
)

http = httplib2.Http(ca_certs=certifi.where(), disable_ssl_certificate_validation=True)
authed_http = AuthorizedHttp(creds, http=http)

service = build("sheets", "v4", http=authed_http)


def get_sheet():
    return service.spreadsheets()
