"""Runner file that is able to put the data together and run the file to return an output"""

__author__ = "Darian Choi, Garrett Buchanan"
__copyright__ = "Copyright 2023, Darian Choi, Garrett Buchanan"
__credits__ = ["Darian Choi, Garrett Buchanan"]
__license__ = "MIT"
__email__ = "dchoi@westmont.edu, gbuch@westmont.edu"

from takeout_models import EmailAnalyzer

def main():
    mbox_file = ('mail.mbox')  # Replace with your mbox file path

    analyzer = EmailAnalyzer(mbox_file)

    top_senders = analyzer.get_top_senders()
    print("Top Senders:")
    for sender, count in top_senders:
        print(f"{sender}: {count} emails")

    top_recipients = analyzer.get_top_recipients()
    print("\nTop Recipients:")
    for recipient, count in top_recipients:
        print(f"{recipient}: {count} emails")

    common_hours = analyzer.get_common_hours()
    print("\nMost Common Hours Emails are Sent:")
    for hour, count in common_hours:
        print(f"{hour}:00 - {hour + 1}:00: {count} emails")

if __name__ == "__main__":
    main()
