"""Main file for sentiment analysis"""

from datetime import datetime as dt
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as p
from pandas.core.frame import DataFrame
from textblob import TextBlob

FE = Path("../data/feminism_data.csv")
NP = Path("../data/NeutralPolitics_data.csv")
TOK = Path("../data/tokyo_2020_tweets_2.csv")
USA = Path("../data/USAelection2024tweets.csv")

def load_file(fp: Path, columns: list[str]):
    df: DataFrame = p.read_csv(fp)
    df["date_str"] = df[columns[1]]
    df["sentiment"] = [TextBlob(str(i) or "").sentiment for i in df[columns[0]]]
    df["sentiment_polarity"] = [i[0] for i in df["sentiment"]]
    df["sentiment_subjectivity"] = [i[1] for i in df["sentiment"]]
    df["date"] = [dt.strptime(i, "%Y-%m-%d %H:%M:%S") for i in df["date_str"]]

    df = df.sort_values("date")

    df["rolling_sentiment_polarity"] = df["sentiment_polarity"].rolling(50).mean()
    df["rolling_sentiment_subjectivity"] = df["sentiment_subjectivity"].rolling(50).mean()
    return df

fe = load_file(FE, ["Body", "creation_date"])
np = load_file(NP, ["Body", "creation_date"])
tok = load_file(TOK, ["text", "date"])
# usa = load_file(USA, ["tweet_text", "timestamp"])

fig, ax = plt.subplots(1, 2)
_ = ax[0].set_xlabel("Date")
_ = ax[0].set_ylabel("Rolling Sentiment Polarity")
_ = ax[0].plot(fe["date"], fe["rolling_sentiment_polarity"], label="Feminism Reddit")
_ = ax[0].plot(np["date"], np["rolling_sentiment_polarity"], label="Neutral Politics Reddit")
_ = ax[0].plot(tok["date"], tok["rolling_sentiment_polarity"], label="Neutral Politics Reddit")
_ = ax[0].legend()

_ = ax[1].set_xlabel("Date")
_ = ax[1].set_ylabel("Rolling Sentiment Subjectivity")
_ = ax[1].plot(fe["date"], fe["rolling_sentiment_subjectivity"], label="Feminism Reddit")
_ = ax[1].plot(np["date"], np["rolling_sentiment_subjectivity"], label="Neutral Politics Reddit")
_ = ax[1].plot(tok["date"], tok["rolling_sentiment_subjectivity"], label="Neutral Politics Reddit")
_ = ax[1].legend()

# _ = fig.savefig("fig2.png")
# fig.show()
plt.show()
