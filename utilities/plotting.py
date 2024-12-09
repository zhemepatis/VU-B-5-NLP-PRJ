from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def plot_word_cloud(wc, word_ctr):
    wc.generate_from_frequencies(word_ctr)

    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    return plt


def plot_bar_chart(ctr, title, x_label, y_label):
    plt.figure(figsize=(12, 6))
    plt.bar(ctr.keys(), ctr.values(), color='teal', markerSize = 6)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation = 45, ha = 'right')

    plt.tight_layout()

    return plt


def plot_histogram(data, title, x_label, y_label, bin_lower_bound = 0, bin_upper_bound = 5, bin_step = 0.5):
    bins = np.arange(bin_lower_bound, bin_upper_bound, bin_step)

    plt.figure(figsize=(10, 6))
    plt.hist(data, bins = bins, color = 'darkblue', edgecolor = 'black', alpha = 0.7)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    return plt