""" Unittests for the data retrieval system takeout"""

__author__ = "Darian Choi, Garrett Buchanan"
__copyright__ = "Copyright 2023, Darian Choi, Garrett Buchanan"
__credits__ = ["Darian Choi, Garrett Buchanan"]
__license__ = "MIT"
__email__ = "dchoi@westmont.edu, gbuch@westmont.edu"

import unittest
from src.takeout.takeout_models import EmailAnalyzer

# Example email data for testing purposes


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        # Creating a temporary mbox file with example emails for testing
        example_emails = [
            {
                'From': 'sender@example.com',
                'To': 'recipient1@example.com',
                'Date': 'Fri, 01 Jan 2023 09:00:00 +0000',
                # Add other necessary email fields for testing
            },
            {
                'From': 'sender@example.com',
                'To': 'recipient2@example.com, recipient3@example.com',
                'Date': 'Sat, 02 Jan 2023 10:00:00 +0000',
                # Add other necessary email fields for testing
            },
            # Add more example emails as needed for testing different scenarios
        ]
        self.test_mbox_path = 'path/to/test/mbox/file.mbox'  # Replace with your test mbox file path


        # Initializing EmailAnalyzer with the test mbox file
        self.analyzer = EmailAnalyzer(self.test_mbox_path)

    def test_top_senders(self):
        top_senders = self.analyzer.get_top_senders(n=1)
        expected_senders = [('sender@example.com', 2)]
        self.assertEqual(top_senders, expected_senders)

    def test_top_recipients(self):
        top_recipients = self.analyzer.get_top_recipients(n=1)
        expected_recipients = [('recipient2@example.com', 1)]
        self.assertEqual(top_recipients, expected_recipients)

    def test_common_hours(self):
        common_hours = self.analyzer.get_common_hours(n=1)
        expected_hours = [(10, 1)]
        self.assertEqual(common_hours, expected_hours)

if __name__ == '__main__':
    unittest.main()
