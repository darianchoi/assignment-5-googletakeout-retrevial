""" data models for information retrieval of email data
"""

__author__ = "Darian Choi, Garrett Buchanan"
__copyright__ = "Copyright 2023, Darian Choi, Garrett Buchanan"
__credits__ = ["Darian Choi, Garrett Buchanan"]
__license__ = "MIT"
__email__ = "dchoi@westmont.edu, gbuch@westmont.edu"

import mailbox
from collections import Counter
from datetime import datetime


class EmailAnalyzer:
    def __init__(self, mbox_file):
        self.emails = mailbox.mbox(mbox_file)

    def get_top_senders(self, n=5):
        sender_counter = Counter()
        for email in self.emails:
            sender = email['From']
            if sender:
                sender_counter[sender] += 1
        return sender_counter.most_common(n)

    def get_top_recipients(self, n=5):
        recipient_counter = Counter()
        for email in self.emails:
            recipients = email['To'].split(', ') if email['To'] else []
            for recipient in recipients:
                if recipient:
                    recipient_counter[recipient] += 1
        return recipient_counter.most_common(n)

    def get_common_hours(self, n=5):
        email_hours = []
        for email in self.emails:
            date_str = email['Date']
            if date_str:
                # Adjusted date format to match 'Tue, 28 Nov 2023 22:31:30'
                date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')
                hour = date.hour
                email_hours.append(hour)
        hour_counter = Counter(email_hours)
        return hour_counter.most_common(n)
