import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import argparse

argsparser = argparse.ArgumentParser(description="Analyze the latency from G2GDelay measurer. ")
argsparser.add_argument("--file", "-f", type=str, default="./results.csv", help="Path to the CSV file with the latency data")
argsparser.add_argument("--window", "-w", type=int, default=1, help="Window size for the moving average")
argsparser.add_argument("--nbins", "-n", type=int, default=15, help="Number of bins for the histogram")
argsparser.add_argument("--percentile", "-p", type=float, default=0.95, help="Percentile for the range plot")
argsparser.add_argument("--remove_outliers", "-r", type=bool, default=False, help="Remove outliers from the data")
argsparser.add_argument("--z-threshold", "-z", type=float, default=3, help="z-score threshold for outlier removal")


BASE_COLOR = sns.color_palette("flare")[5]
MEAN_COLOR = sns.color_palette("flare")[3]
FILL_COLOR = sns.color_palette("flare")[0]
PERC_COLOR = sns.color_palette("flare")[2]


def plot_latency_statistics(args):
    file_path = args.file
    window_size = args.window
    
    data = pd.read_csv(file_path)

    data['latency'] = data['latency'].rolling(window=window_size).mean().dropna()
    data['Index'] = data.index

    if args.remove_outliers:
        z_scores = (data['latency'] - data['latency'].mean()) / data['latency'].std()
        threshold = args.z_threshold

        data = data.loc[abs(z_scores) <= threshold]

    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(14, 8))

    sns.lineplot(x='Index', y='latency', data=data, color=BASE_COLOR, lw=1.5, linestyle='-')
    sns.scatterplot(x='Index', y='latency', data=data, color=BASE_COLOR, s=20, alpha=0.7)

    mean_latency = data['latency'].mean()
    std_deviation = data['latency'].std()
    min_latency = data['latency'].min()
    max_latency = data['latency'].max()
    median_latency = data['latency'].median()

    plt.axhline(y=mean_latency, color=MEAN_COLOR, linestyle='-', linewidth=4, label=f'Mean: {mean_latency:.2f}')
    plt.fill_between(data['Index'], mean_latency - std_deviation, mean_latency + std_deviation, color=PERC_COLOR, alpha=0.3, label='1 STD Range')

    percentile = args.percentile
    lower_limit = data['latency'].quantile(1-percentile)
    upper_limit = data['latency'].quantile(percentile)

    plt.fill_between(data['Index'], lower_limit, upper_limit, color=FILL_COLOR, alpha=0.3, label=f'{int(percentile*100)}% of Data')

    text_stats = f'Mean:   {mean_latency:.2f} ms\nMedian:   {median_latency:.2f} ms\nStandard Deviation:   {std_deviation:.2f} ms\nMax:   {max_latency:.2f} ms\nMin:   {min_latency:.2f} ms'
    plt.text(0.5, 0.95, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    plt.text(0.95, mean_latency+std_deviation, f'{mean_latency + std_deviation:.2f}', fontsize=12,  horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    plt.text(0.95, mean_latency-std_deviation, f'{mean_latency - std_deviation:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    plt.text(0.95, mean_latency+0.1*std_deviation, f'{mean_latency:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    plt.legend(title="Latency Statistics", title_fontsize='large', fontsize='large')

    stats_df = pd.DataFrame({
        'Statistic': ['Samples', 'Mean', 'Median', 'Standard Deviation', 'Max', 'Min'],
        'Value': [len(data), mean_latency, median_latency, std_deviation, max_latency, min_latency]
    })

    plt.title('Latency Analysis', fontsize=20, color='navy', loc='left')
    plt.xlabel('Time (Samples)', fontsize=14)
    plt.ylabel('Latency (ms)', fontsize=14)
    plt.legend(title="Latency Statistics")
    plt.grid(False)

    sns.despine()
    plt.show()


def plot_latency_histogram(args):

    file_path = args.file
    n_bins = args.nbins

    data = pd.read_csv(file_path)

    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(14, 8))

    sns.histplot(data, bins=n_bins, color=BASE_COLOR, kde=True, fill=True, edgecolor='black', linewidth=1.5)

    mean_latency = data['latency'].mean()
    std_deviation = data['latency'].std()
    min_latency = data['latency'].min()
    max_latency = data['latency'].max()
    median_latency = data['latency'].median()

    text_stats = f'Mean: {mean_latency:.2f}\nMedian: {median_latency:.2f}\nStandard Deviation: {std_deviation:.2f}\nMax: {max_latency:.2f}\nMin: {min_latency:.2f}'
    plt.text(0.95, 0.5, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    plt.title('Latency Distribution', fontsize=20, color='navy', loc='left')
    plt.xlabel('Latency (ms)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)


    sns.despine()
    plt.grid(False)
    plt.show()


def plot_both(args):
    
    file_path = args.file
    window_size = args.window
 
    data = pd.read_csv(file_path)

    
    data['latency'] = data['latency'].rolling(window=window_size).mean().dropna()
    data['Index'] = data.index

    if args.remove_outliers:
        z_scores = (data['latency'] - data['latency'].mean()) / data['latency'].std()
        threshold = args.z_threshold

        data = data[(np.abs(z_scores) < threshold)]


    sns.set_theme(style='whitegrid')
    fig, axs = plt.subplots(1, 2, figsize=(20, 8), width_ratios=[2, 1])

    sns.lineplot(ax=axs[0], x='Index', y='latency', data=data, color=BASE_COLOR, lw=1.5, linestyle='-')
    sns.scatterplot(ax=axs[0], x='Index', y='latency', data=data, color=BASE_COLOR, s=20, alpha=0.7)

    mean_latency = data['latency'].mean()
    std_deviation = data['latency'].std()
    min_latency = data['latency'].min()
    max_latency = data['latency'].max()
    median_latency = data['latency'].median()


    axs[0].axhline(y=mean_latency, color=MEAN_COLOR, linestyle='-', linewidth=4, label=f'Mean')
    axs[0].fill_between(data['Index'], mean_latency - std_deviation, mean_latency + std_deviation, color=PERC_COLOR, alpha=0.3, label='1 STD Range')

    percentile = args.percentile
    lower_limit = data['latency'].quantile(1-percentile)
    upper_limit = data['latency'].quantile(percentile)

    axs[0].fill_between(data['Index'], lower_limit, upper_limit, color=FILL_COLOR, alpha=0.3, label=f'{int(percentile*100)}% of Data')

    axs[0].text(0.95, mean_latency+std_deviation, f'{mean_latency + std_deviation:.2f}', fontsize=12,  horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    axs[0].text(0.95, mean_latency-std_deviation, f'{mean_latency - std_deviation:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    axs[0].text(0.95, mean_latency+0.1*std_deviation, f'{mean_latency:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))


    axs[0].legend(title="Latency Statistics", title_fontsize='large', fontsize='large')
    axs[0].set_title('Latency Analysis', fontsize=20, color='navy', loc='left')
    axs[0].set_xlabel('Time (Samples)', fontsize=14)
    axs[0].set_ylabel('Latency (ms)', fontsize=14)
    axs[0].grid(False)

    # Removing the top and right spines for a cleaner look
    # sns.despine(ax=axs[0])

    # Creating the histogram plot

    n_bins = args.nbins
    sns.histplot(data, ax=axs[1], y='latency', bins=n_bins, color=BASE_COLOR, kde=True, fill=True, edgecolor='black', linewidth=1.5)

    text_stats = f'Mean: {mean_latency:.2f}\nMedian: {median_latency:.2f}\nStandard Deviation: {std_deviation:.2f}\nMax: {max_latency:.2f}\nMin: {min_latency:.2f}'
    axs[1].text(0.95, 0.75, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    axs[1].set_title('Latency Distribution', fontsize=20, color='navy', loc='left')
    axs[1].set_xlabel('Frequency', fontsize=14)
    axs[1].set_ylabel('Latency (ms)', fontsize=14)


    sns.despine()
    plt.grid(False)
    # plt.savefig(f'{file_path[:-4]}_analysis.svg')
    plt.show()


if __name__ == "__main__":
    import sys

    args = argsparser.parse_args(sys.argv[1:])
    # plot_latency_statistics(args)
    # plot_latency_histogram(args)
    plot_both(args)