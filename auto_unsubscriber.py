#! python3
# filename.py — Short description of project goes here.
# For more information, see project_details.txt.

from datetime import date
import logging
import os
import webbrowser
from bs4 import BeautifulSoup
from imapclient import IMAPClient
from pyzmail import PyzMessage

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
# logging.disable(logging.DEBUG)  # Note out to enable logging.

IMAP_HOST = os.environ.get("ICLD_IMAP")
IMAP_ADDRESS = os.environ.get("ICLD_USER")
IMAP_PASSWORD = os.environ.get("ICLD_PASS")

SEARCH_BEGIN_DATE = date(2023, 5, 1)

unsubscribe_urls = []

with IMAPClient(IMAP_HOST) as client:
    client.login(IMAP_ADDRESS, IMAP_PASSWORD)
    client.select_folder("INBOX", readonly=True)
    email_ids = client.search(["SINCE", SEARCH_BEGIN_DATE])

    for email_id in email_ids:
        raw_message = client.fetch([email_id], ["BODY[]", "FLAGS"])
        message = PyzMessage.factory(raw_message[email_id][b"BODY[]"])
        if message.html_part is not None:
            html_msg = message.html_part.get_payload().decode(message.html_part.charset)
            soup = BeautifulSoup(html_msg, features="html.parser")
            for link in soup.find_all("a", string=["Unsubscribe", "unsubscribe"]):
                unsubscribe_urls.append(link.get("href"))

for url in unsubscribe_urls:
    webbrowser.open(url)
