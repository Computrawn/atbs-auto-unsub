#! python3
# filename.py — Short description of project goes here.
# For more information, see project_details.txt.

from datetime import date
import logging
import os
from imapclient import IMAPClient
import pyzmail

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
logging.disable(logging.DEBUG)  # Note out to enable logging.

IMAP_HOST = os.environ.get("ICLD_IMAP")
IMAP_ADDRESS = os.environ.get("ICLD_USER")
IMAP_PASSWORD = os.environ.get("ICLD_PASS")

with IMAPClient(IMAP_HOST) as client:
    client.login(IMAP_ADDRESS, IMAP_PASSWORD)
    client.select_folder("INBOX", readonly=True)
    UIDs = client.search(["SINCE", date(2023, 5, 1)])

    for uid in UIDs:
        raw_message = client.fetch([uid], ["BODY[]", "FLAGS"])
        message = pyzmail.PyzMessage.factory(raw_message[uid][b"BODY[]"])
        if message.html_part is not None:
            logging.info(
                message.html_part.get_payload().decode(message.html_part.charset)
            )
