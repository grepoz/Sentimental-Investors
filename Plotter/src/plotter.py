import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np
mpl.rcParams['lines.linewidth'] = 3


class Plotter:

    @staticmethod
    def plot(df, chart_filepath, token):

        fig, ax1 = plt.subplots(figsize=(16, 8), dpi=200)
        plt.title(f"Correlation between sentiment and stock price for {token}")

        ax1.plot(df.VaderSentiment, color="blue", label="Vader sentiment", linewidth=1)
        ax1.plot(df.FlairSentiment, color="orange", label="Flair sentiment", linewidth=1)
        ax1.plot(df.ScaledClose, color="green", label="Close price")
        ax2 = ax1.twinx()
        ax2.plot(df.Close, color="brown", label="Close price", alpha=0.0)

        # calculate equation for trendline
        vader_y = df.VaderSentiment.values
        flair_y = df.FlairSentiment.values
        x = [i for i in range(len(vader_y))]
        vader_z = np.polyfit(x, vader_y, 16)
        vader_p = np.poly1d(vader_z)
        ax1.plot(x, vader_p(x), color='purple', label="Vader trend line")

        flair_z = np.polyfit(x, flair_y, 16)
        flair_p = np.poly1d(flair_z)
        ax1.plot(x, flair_p(x), color='yellow', label="Flair trend line")

        ax1.set_xlabel("date", fontsize=14)
        ax1.set_ylabel("sentiment (<-1,1>)", fontsize=14)
        ax1.legend(loc='upper left')
        ax1.axhline(y=0, color='r', linestyle='dashed', linewidth=1)

        ax2.set_ylabel("stock price ($)", fontsize=14)
        # ax2.legend(loc=0)
        fig.autofmt_xdate()
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=4))
        fig.savefig(f"{chart_filepath}.png")
        plt.show()
