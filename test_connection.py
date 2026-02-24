import os
import certifi
import httplib2
import ssl
import traceback

ssl._create_default_https_context = ssl._create_unverified_context

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google_auth_httplib2 import AuthorizedHttp

def test():
    try:
        # ✅ FORCE CERT PATH
        os.environ["SSL_CERT_FILE"] = certifi.where()
        os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        SPREADSHEET_ID = "1PTQBIW4wGSy5UsbPt5FxFEyfW_Vl3uyUdHiVcwQbPfE"

        print(f"Using SPREADSHEET_ID: {SPREADSHEET_ID}")
        print(f"Service account exists: {os.path.exists('service_account.json')}")

        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=SCOPES
        )

        http = httplib2.Http(ca_certs=certifi.where(), disable_ssl_certificate_validation=True)
        authed_http = AuthorizedHttp(creds, http=http)

        service = build("sheets", "v4", http=authed_http)
        
        print("Testing get request...")
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="Users!A:E"
        ).execute()
        print("Success! Data retrieved:")
        for i, row in enumerate(result.get("values", [])):
            print(f"Row {i}: {row}")
        
    except Exception as e:
        print(f"FAILED: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    test()
