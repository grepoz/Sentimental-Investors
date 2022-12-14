from flair.models import TextClassifier
from flair.data import Sentence
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all",  # Capitalized negation,
             "bitcoin has raised by 20%",
             "bitcoin has dropped by 20%",
             "bitcoin is neutral",
             "is neutral",
             "incredibly raise in intel",
             "market is bullish",
             ]

vaderAnalyzer = SentimentIntensityAnalyzer()
classifier = TextClassifier.load('en-sentiment')


def get_sentiment(text, is_vader=True):
    if is_vader:
        return vaderAnalyzer.polarity_scores(text)['compound']
    else:
        text = Sentence(text)
        classifier.predict(text)
        value = text.labels[0].to_dict()['value']
        if value == 'POSITIVE':
            result = text.to_dict()['all labels'][0]['confidence']
        else:
            result = -(text.to_dict()['all labels'][0]['confidence'])
        return round(result, 3)
