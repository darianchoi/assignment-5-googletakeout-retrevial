""""Implementation of a simple classifier."""

__authors__ = "Garrett Buchanan" "Darian Choi"
__credits__ = ["Mike Ryu, Garrett Buchanan, Darian Choi"]
__email__ = "gbuchanan@westmont.edu" "dchoi@westmont.edu"

# SNAIL
from collections import defaultdict, Counter
from math import log10
from typing import Iterable, Any
from classifier.classifier_models import Feature, FeatureSet, AbstractClassifier
from nltk import word_tokenize


class OurFeature(Feature):
    pass


class OurFeatureSet(FeatureSet):

    @classmethod
    def build(cls, source_object: Any, known_clas=None, **kwargs) -> FeatureSet:
        """
        :param source_object: object to build the feature set from
        :param known_clas: pre-defined classification of the source object
        :param kwargs: any additional data needed to preprocess the `source_object` into a feature set
        :return: an instance of `FeatureSet` built based on the `source_object` passed in
        """

        features = set()

        words = word_tokenize(source_object)
        sender = recipient = subject = None

        for i, word in enumerate(words):
            # if words[i:i + 2] == ['From', ':']:
            #     sender = words[i + 2:]
            # elif words[i:i + 2] == ['To', ':']:
            #     recipient = words[i + 2:]
            # elif words[i:i + 2] == ['Subject', ':']:
            #     subject = words[i + 2:]

            token = word.lower()  # Convert word to lowercase for consistency
            word_len = len(token)

            # Add individual words as features
            features.add(Feature(name=f"contains {token}", value=True))


        return cls(features, known_clas)


class OurClassifier(AbstractClassifier):

    def __init__(self, class_word_counts, class_total_words, classes, feature_probabilities):
        self.classes = classes
        self.class_total_words = class_total_words
        self.class_word_counts = class_word_counts
        self.feature_probabilities = feature_probabilities
        self.stored_ratio = {}

    def gamma(self, feat_set: OurFeatureSet) -> str:
        """ takes in a feature set then iterates through each feature and then
        calculates the probability of it mapping to each class"""
        highest_probability = 0.0
        predicted_class = ''
        for cls in self.classes:
            probability = 0.0  # Probability for the current class
            for feature in feat_set.feat:
                if feature.name not in self.feature_probabilities:
                    pass
                else:
                    feature_prob = self.feature_probabilities[feature.name][cls]  # access the probability
                    probability += log10(feature_prob + 1)

                    if probability > highest_probability:
                        highest_probability = probability
                        predicted_class = cls
        return predicted_class

    def return_present_features(self, top_n: int = 1) -> str:
        """Prints `top_n` feature(s) used by this classifier in the descending order of informativeness of the
        feature in determining a class for any object. Informativeness of a feature is a quantity that represents
        how "good" a feature is in determining the class for an object.

        :param top_n: how many of the top features to print; must be 1 or greater
        """
        ratio_list = []

        for feature, class_probabilities in self.feature_probabilities.items():
            positive_prob = class_probabilities["gbuch"]
            negative_prob = class_probabilities["dchoi"]
            if positive_prob == 0 or negative_prob == 0:
                continue

            if negative_prob >= positive_prob:
                ratio = negative_prob / positive_prob
                formatted_ratio = ("dchoi:gbuch", ratio)
            else:
                ratio = positive_prob / negative_prob
                formatted_ratio = ("gbuch:dchoi", ratio)

            ratio_list.append((feature, formatted_ratio))

        sorted_ratios = sorted(ratio_list, key=lambda item: item[1][1], reverse=True)

        top_n_ratios = sorted_ratios[:top_n]
        return_values = ""
        for feature, ratio in top_n_ratios:
            ratio_label, ratio_value = ratio
            return_value = f"{feature}: {ratio_label} = {ratio_value:.2f}:1\n"
            return_values += return_value
        return return_values

    def present_features(self, top_n: int = 1) -> None:
        print(self.return_present_features(top_n))

    @classmethod
    def train(cls, training_set: Iterable[FeatureSet]) -> AbstractClassifier:
        """Method that builds a Classifier instance with its training (supervised learning) already completed. That is,
        the `AbstractClassifier` instance returned as the result of invoking this method must support `gamma` and
        present_features` method calls immediately without needing any other method invocations prior to them.

        :param training_set: An iterable collection of `FeatureSet` to use for training the classifier
        :return: an instance of `AbstractClassifier` with its training already completed

        """
        class_word_counts = defaultdict(Counter)
        class_total_words = {"gbuch": 0, "dchoi": 0}
        classes = ("gbuch", "dchoi")
        feature_probabilities = {}
        if training_set is None:
            raise ValueError
        else:
            for feat_set in training_set:
                cls_name = feat_set.clas
                for feature in feat_set.feat:
                    class_word_counts[cls_name][feature.name] += 1
                    class_total_words[cls_name] += 1

            for unique in classes:
                for feat_set in training_set:  # Loop through all feature sets again
                    for feature in feat_set.feat:
                        word = feature.name  # Extract the word of the feature
                        word_count = class_word_counts[unique][word]
                        class_total = class_total_words[unique]
                        if class_total != 0:
                            score = word_count / class_total
                            if feature.name not in feature_probabilities:
                                feature_probabilities[feature.name] = {}
                            feature_probabilities[feature.name][unique] = score
                        else:
                            score = 0
                            if feature.name not in feature_probabilities:
                                feature_probabilities[feature.name] = {}
                            feature_probabilities[feature.name][unique] = score

        return cls(class_word_counts, class_total_words, classes, feature_probabilities)
