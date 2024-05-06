import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_latency_statistics(file_path, window_size=10):
    # Load the data
    data = pd.read_csv(file_path)

    # Filter the data for a smoother curve
    data['latency'] = data['latency'].rolling(window=window_size).mean().dropna()
    data['Index'] = data.index  # Create an index column for smoother curve generation
    # Setting up a stylish and clean appearance
    sns.set_theme(style='whitegrid')

    # Setting the figure size for better visualization
    plt.figure(figsize=(14, 8))

    # Defining a more subdued and professional color palette
    base_color = sns.color_palette("flare")[5]
    mean_color = sns.color_palette("flare")[3]
    fill_color = sns.color_palette("flare")[0]
    perc_color = sns.color_palette("flare")[2]

    # Creating a smooth line plot
    sns.lineplot(x='Index', y='latency', data=data, color=base_color, lw=1.5, linestyle='-')
    sns.scatterplot(x='Index', y='latency', data=data, color=base_color, s=20, alpha=0.7)

    # Calculate the mean and standard deviation
    mean_latency = data['latency'].mean()
    std_deviation = data['latency'].std()
    min_latency = data['latency'].min()
    max_latency = data['latency'].max()
    median_latency = data['latency'].median()

    # Plotting the mean and standard deviation areas
    plt.axhline(y=mean_latency, color=mean_color, linestyle='-', linewidth=4, label=f'Mean: {mean_latency:.2f}')
    # Plotting the variance lines
    plt.fill_between(data['Index'], mean_latency - std_deviation, mean_latency + std_deviation, color=perc_color, alpha=0.3, label='1 STD Range')

    # Find the limits of 85  percent of the data
    percentile = 0.95
    lower_limit = data['latency'].quantile(1-percentile)
    upper_limit = data['latency'].quantile(percentile)

    # Plotting the 85% of the data
    plt.fill_between(data['Index'], lower_limit, upper_limit, color=fill_color, alpha=0.3, label=f'{int(percentile*100)}% of Data')


    # Adding a legend with the statistics
    text_stats = f'Mean:   {mean_latency:.2f} ms\nMedian:   {median_latency:.2f} ms\nStandard Deviation:   {std_deviation:.2f} ms\nMax:   {max_latency:.2f} ms\nMin:   {min_latency:.2f} ms'
    plt.text(0.5, 0.95, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    plt.text(0.95, mean_latency+std_deviation, f'{mean_latency + std_deviation:.2f}', fontsize=12,  horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    plt.text(0.95, mean_latency-std_deviation, f'{mean_latency - std_deviation:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))
    plt.text(0.95, mean_latency+0.1*std_deviation, f'{mean_latency:.2f}', fontsize=12, horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    # Adding a legend with the statistics
    plt.legend(title="Latency Statistics", title_fontsize='large', fontsize='large')

    # Creating a table with the statistics
    stats_df = pd.DataFrame({
        'Statistic': ['Samples', 'Mean', 'Median', 'Standard Deviation', 'Max', 'Min'],
        'Value': [len(data), mean_latency, median_latency, std_deviation, max_latency, min_latency]
    })

    # Plotting the table


    # Customizing the plot with titles and labels
    plt.title('Latency Analysis', fontsize=20, color='navy', loc='left')
    plt.xlabel('Time (Samples)', fontsize=14)
    plt.ylabel('Latency (ms)', fontsize=14)
    plt.legend(title="Latency Statistics")
    plt.grid(False)

    # Removing the top and right spines for a cleaner look
    sns.despine()

    # Show the plot
    plt.show()


def plot_histogram(file_path, n_bins=15):

    data = pd.read_csv(file_path)
    # Setting up a stylish and clean appearance
    sns.set_theme(style='whitegrid')

    # Setting the figure size for better visualization
    plt.figure(figsize=(14, 8))

    # Defining a more subdued and professional color palette
    base_color = sns.color_palette("flare")[5]
    fill_color = sns.color_palette("flare")[0]

    # Creating a histogram plot
    sns.histplot(data, bins=n_bins, color=base_color, kde=True, fill=True, edgecolor='black', linewidth=1.5)

    # Calculate the mean and standard deviation
    mean_latency = data['latency'].mean()
    std_deviation = data['latency'].std()
    min_latency = data['latency'].min()
    max_latency = data['latency'].max()
    median_latency = data['latency'].median()

    # Adding statistics as text on the side
    text_stats = f'Mean: {mean_latency:.2f}\nMedian: {median_latency:.2f}\nStandard Deviation: {std_deviation:.2f}\nMax: {max_latency:.2f}\nMin: {min_latency:.2f}'
    plt.text(0.95, 0.5, text_stats, fontsize=12, horizontalalignment='right',transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black', alpha=0.5))

    # Customizing the plot with titles and labels
    plt.title('Latency Distribution', fontsize=20, color='navy', loc='left')
    plt.xlabel('Latency (ms)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)

    # Removing the top and right spines for a cleaner look
    sns.despine()

    # Show the plot
    plt.grid(False)
    plt.show()

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv>")
    else:
        file_path = sys.argv[1]
        plot_latency_statistics(file_path)
        # plot_histogram(file_path)
