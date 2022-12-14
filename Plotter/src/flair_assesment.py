from flair.models import TextClassifier
from flair.data import Sentence
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

columns_names = ["Sentence", "Expected result", "VADER", "Flair"]


def __to_dataframe(_data) -> pd.DataFrame:
    df = pd.DataFrame(_data, columns=columns_names, dtype=pd.StringDtype())
    return df


sentences = [
    ["VADER is smart, handsome, and funny.", "positive"],  # positive sentence example
    ["VADER is smart, handsome, and funny!", "positive"],
    # punctuation emphasis handled correctly (sentiment intensity adjusted)
    ["VADER is very smart, handsome, and funny.", "positive"],
    # booster words handled correctly (sentiment intensity adjusted)
    ["VADER is VERY SMART, handsome, and FUNNY.", "positive"],  # emphasis for ALLCAPS handled
    ["VADER is VERY SMART, handsome, and FUNNY!!!", "positive"],
    # combination of signals - VADER appropriately adjusts intensity
    ["VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", "positive"],
    # booster words & punctuation make this close to ceiling for score
    ["VADER is not smart, handsome, nor funny.", "negative"],  # negation sentence example
    ["The book was good.", "positive"],  # positive sentence
    ["At least it isn't a horrible book.", "neutral"],  # negated negative sentence with contraction
    ["The book was only kind of good.", "rather positive"],
    # qualified positive sentence is handled correctly (intensity adjusted)
    ["The plot was good, but the characters are uncompelling and the dialog is not great.", "neutral (mixed)"],
    # mixed negation sentence
    ["Today SUX!", "negative"],  # negative slang with capitalization emphasis
    ["Today only kinda sux! But I'll get by, lol", "neutral (mixed)"],
    # mixed sentiment example with slang and constrastive conjunction "but"
    ["Make sure you :) or :D today!", "positive"],  # emoticons handled
    ["Not bad at all", "neutral"],  # Capitalized negation
    ["$AAPL Attempting a breakout to the upside, now green on the day!", "positive"],
    ["Apple\u2019s, $AAPL, most in-demand iPhones will fall short of earlier shipment estimates by 6 million units", "negative"],
    ["$AAPL Threatening a red to green move this morning, keep an eye on this descending triangle setup",
     "positive"],
    ["Most Traded Contracts $AAPL November $150 Call, $TSLA November $200 Call, $AMZN January 2023 $140 Put", "neutral"]

]

vaderAnalyzer = SentimentIntensityAnalyzer()
classifier = TextClassifier.load('en-sentiment')

data = [["", "", "", ""]]
data = __to_dataframe(data)

cnt = 1
for sentence in sentences:
    vader_score = vaderAnalyzer.polarity_scores(sentence[0])['compound']
    flair_sentence = Sentence(sentence[0])
    classifier.predict(flair_sentence)

    row = [
        sentence[0],
        sentence[1],
        round(vader_score, 3),
        str(flair_sentence.labels[0].to_dict()['value'])[:3] + ": " + str(round(flair_sentence.to_dict()['all labels'][0]['confidence'], 3))
    ]

    data.loc[len(data.index)] = row
    print(f'Sentence: {sentence[0]}')
    print(f'Expected result: {sentence[1]}')
    print(f'VADER: {vader_score}, Flair: ' + str(flair_sentence.labels[0].to_dict()['value']) + ": " + str(
        round(flair_sentence.to_dict()['all labels'][0]['confidence'], 3)))
    print()
    cnt += 1

data['index'] = data.index
data.set_index('index', inplace=True)
data.drop(0, axis=0, inplace=True)
data.to_csv("manual_analysis.csv")
