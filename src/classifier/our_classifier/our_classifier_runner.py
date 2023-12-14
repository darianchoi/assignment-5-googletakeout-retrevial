"Runner for classifier"
import mailbox
import os
import pickle
import quopri
import random

from bs4 import BeautifulSoup

from classifier.our_classifier.our_classifier_models import OurFeatureSet, OurClassifier

__author__ = "Darian Choi, Garrett Buchanan"
__copyright__ = "Copyright 2023, Westmont College, Mike Ryu"
__credits__ = ["Mike Ryu"]
__license__ = "MIT"
__email__ = "dchoi@westmont.edu, gbuchanan@westmont.edu"


def main() -> None:
    raw_emails_gbuch = []
    raw_emails_dchoi = []
    cache_file = '../../../data/classifier_cache.pkl'
    if os.path.exists(cache_file):
        # Load cached classifier and feature sets
        with open(cache_file, 'rb') as f:
            classifier, train_set, test_set = pickle.load(f)
    else:

        mbox_file_gbuch = '../../../../Inbox.mbox'
        mbox_file_dchoi = '../../../../mail.mbox'

        # Load the MBOX file
        mbox_g = mailbox.mbox(mbox_file_gbuch)
        mbox_d = mailbox.mbox(mbox_file_dchoi)
        # CHAT GPT: "i only want 2000 emails from each"
        # from lines 38-50

        # Iterate through each email in the MBOX file
        MAX_EMAILS = 2000  # Define the maximum number of emails to retrieve

        for index, message in enumerate(mbox_g):
            if index >= MAX_EMAILS:
                break
            email_content_gbuch = extract_visible_text(message)
            raw_emails_gbuch.append(email_content_gbuch)

        for index, message in enumerate(mbox_d):
            if index >= MAX_EMAILS:
                break
            email_content_dchoi = extract_visible_text(message)
            raw_emails_dchoi.append(email_content_dchoi)

        # building the feature sets to use
        gbuch_sets = [OurFeatureSet.build(tweet, 'gbuch') for tweet in raw_emails_gbuch]
        dchoi_sets = [OurFeatureSet.build(tweet, 'dchoi') for tweet in raw_emails_dchoi]

        # Combine positive and negative feature sets
        all_featuresets = gbuch_sets + dchoi_sets
        # shuffle and randomize so you get authentic results
        random.shuffle(all_featuresets)
        train_set, test_set = all_featuresets[1600:], all_featuresets[:400]

        classifier = OurClassifier.train(train_set)
        with open(cache_file, 'wb') as f:
            pickle.dump((classifier, train_set, test_set), f)
    total_instances = len(test_set)
    correct_predictions = 0

    for instance in test_set:
        predicted_class = classifier.gamma(instance)
        if predicted_class == instance.clas:
            correct_predictions += 1

    accuracy = (correct_predictions / total_instances) * 100
    print(f"Accuracy: {accuracy}%")

    classifier.present_features(30)
    while True:  # asked chat gpt how to allow me to keep querying
        email_content = input("Enter email content (or type 'exit' to quit):  ")

        if email_content.lower() == 'exit':
            print("Exiting...")
            break

        email_features = OurFeatureSet.build(email_content)
        predicted_inbox = classifier.gamma(email_features)

        if predicted_inbox == "":
            print(
                "Sorry, there was not enough information to determine which email it belongs to. Could you provide more content?")
        else:
            print(f"This email most likely belongs to: {predicted_inbox}")


def extract_visible_text(part):
    text = ""
    if part.is_multipart():
        for subpart in part.get_payload():
            text += extract_visible_text(subpart)
    else:
        content_type = part.get_content_type()
        if content_type == "text/plain":
            try:
                decoded_bytes = quopri.decodestring(part.get_payload())
                text += decoded_bytes.decode('utf-8')
            except (UnicodeDecodeError, ValueError):
                text += part.get_payload(decode=True).decode('latin1', 'ignore')

        elif content_type == "text/html":
            soup = BeautifulSoup(part.get_payload(), 'html5lib')
            text += soup.get_text()

    return text


if __name__ == '__main__':
    main()
