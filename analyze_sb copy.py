import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_latency_and_histogram(file_path, window_size=1, n_bins=15):
    # Load the data
    data = pd.read_csv(file_path)

    # Filter the data for a smoother curve
    data['latency'] = data['latency'].rolling(window=window_size).mean().dropna()
    data['Index'] = data.index  # Create an index column for smoother curve generation

    # Setting up a stylish and clean appearance
    sns.set_theme(style='whitegrid')

    # Setting the figure size for better visualization
    fig, axs = plt.subplots(1, 2, figsize=(20, 8), width_ratios=[2, 1])

    # Defining a more subdued and professional color palette
    base_color = sns.color_palette("flare")[5]
    mean_color = sns.color_palette("flare")[3]
    fill_color = sns.color_palette("flare")[0]
    perc_color = sns.color_palette("flare")[2]

    # Creating a smooth line plot   
    sns.lineplot(ax=axs[0], x='Index', y='latency', data=data, color=base_color, lw=1.5, linestyle='-')
    sns.scatterplot(ax=axs[0], x='Index', y='latency', data=data, color=base_color, s=20, alpha=0.7)

    # Calculate the mean and standard deviation
    mean_latency = data['latency'].mean()
    std_deviation = data['latency'].std()
    min_latency = data['latency'].min()
    max_latency = data['latency'].max()
    median_latency = data['latency'].median()

    # Plotting the mean and standard deviation areas
    axs[0].axhline(y=mean_latency, color=mean_color, linestyle='-', linewidth=4, label=f'Mean')
    # Plotting the variance lines
    axs[0].fill_between(data['Index'], mean_latency - std_deviation, mean_latency + std_deviation, color=perc_color, alpha=0.3, label='1 STD Range')

    # Find the limits of 85  percent of the data
    percentile = 0.95
    lower_limit = data['latency'].quantile(1-percentile)
    upper_limit = data['latency'].quantile(percentile)

    # Plotting the 85% of the data
    axs[0].fill_between(data['Index'], lower_limit, upper_limit, color=fill_color, alpha=0.3, label=f'{int(percentile*100)}% of Data')

    # Adding a legend with the statistics
    # text_stats = f'Mean:   {mean_latency:.2f} ms\nMedian:   {median_latency:.2f} ms\nStandard Deviation:   {std_deviation:.2f} ms\nMax:   {max_latency:.2f} ms\nMin:   {min_latency:.2f} ms'
    # plt.text(0.5, 0.95, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    axs[0].text(0.95, mean_latency+std_deviation, f'{mean_latency + std_deviation:.2f}', fontsize=12,  horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    axs[0].text(0.95, mean_latency-std_deviation, f'{mean_latency - std_deviation:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    axs[0].text(0.95, mean_latency+0.1*std_deviation, f'{mean_latency:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    # Adding a legend with the statistics
    axs[0].legend(title="Latency Statistics", title_fontsize='large', fontsize='large')

    # Customizing the plot with titles and labels
    axs[0].set_title('Latency Analysis', fontsize=20, color='navy', loc='left')
    axs[0].set_xlabel('Time (Samples)', fontsize=14)
    axs[0].set_ylabel('Latency (ms)', fontsize=14)
    axs[0].grid(False)

    # Removing the top and right spines for a cleaner look
    # sns.despine(ax=axs[0])

    # Creating a histogram plot
    sns.histplot(data, ax=axs[1], y='latency', bins=n_bins, color=base_color, kde=True, fill=True, edgecolor='black', linewidth=1.5)

    # Adding statistics as text on the side
    text_stats = f'Mean: {mean_latency:.2f}\nMedian: {median_latency:.2f}\nStandard Deviation: {std_deviation:.2f}\nMax: {max_latency:.2f}\nMin: {min_latency:.2f}'
    axs[1].text(0.95, 0.75, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    # Customizing the plot with titles and labels
    axs[1].set_title('Latency Distribution', fontsize=20, color='navy', loc='left')
    axs[1].set_xlabel('Frequency', fontsize=14)
    # axs[1].get_yaxis().set_visible(False)
    axs[1].set_ylabel('Latency (ms)', fontsize=14)

    # Removing the top and right spines for a cleaner look
    sns.despine()

    # Show the plot
    plt.grid(False)
    plt.savefig(f'{file_path[:-4]}_analysis.svg')
    # plt.show()

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv>")
        paths = [r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_mjpeg_320x320_30fps_clean.csv",
                 r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_mjpeg_1280x720_30fps_clean.csv",
                 r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_mjpeg_1920x1080_30fps_clean.csv",
                 r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_uncompressed_320x320_30fps_clean.csv",
                 r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_uncompressed_1280x720_30fps_clean.csv",
                 r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_uncompressed_320x320_60fps_clean.csv",
                 r"D:\Data\Dev\MarineVisionAI\examples\data\Testing\Latency\results_uncompressed_1280x720_60fps_clean.csv"]
        for path in paths:
            plot_latency_and_histogram(path)
    else:
        file_path = sys.argv[1]
        plot_latency_and_histogram(file_path)
