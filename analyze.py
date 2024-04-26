import pandas as pd
import matplotlib.pyplot as plt

def plot_latency_statistics(file_path):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)
    
    # Calculate statistics
    num_samples = len(data)
    mean_latency = data['latency'].mean()
    median_latency = data['latency'].median()
    std_deviation = data['latency'].std()
    max_latency = data['latency'].max()
    min_latency = data['latency'].min()

    # Create the plot
    plt.figure(figsize=(10, 10))
    plt.plot(range(len(data)), data['latency'], alpha=0.7, color='blue', label='Latency Points')
    
    # Highlight the mean and median
    plt.axhline(y=mean_latency, color='r', linestyle='-', label=f'Mean: {mean_latency:.2f}')
    plt.axhline(y=median_latency, color='g', linestyle='--', label=f'Median: {median_latency:.2f}')
    
    # Annotating statistics
    # Create a DataFrame for the statistics
    stats_df = pd.DataFrame({
        'Statistic': ['Samples', 'Mean', 'Median', 'Standard Deviation', 'Max', 'Min'],
        'Value': [num_samples, mean_latency, median_latency, std_deviation, max_latency, min_latency]
    })

    # Display the statistics table
    table = plt.table(cellText=stats_df.values,
              colLabels=stats_df.columns,
              cellLoc='center',
              loc='bottom',
              bbox=[0, -0.5, 1, 0.4],
              )
    
    # Adjust the plot layout
    plt.subplots_adjust(bottom=0.35)

    # Annotating statistics
    stats_text = f"Mean =  {mean_latency:.2f}\nMedian = {median_latency:.2f}\nStandard Deviation = {std_deviation:.2f}\nMax = {max_latency:.2f}\nMin = {min_latency:.2f}"
    #plt.figtext(0.15, 0.6, stats_text, bbox=dict(facecolor='white', alpha=0.5))
    
    # Print the statistics in terminal
    print(stats_text)
    
    
    
    # Setting titles and labels
    plt.title('Latency Analysis')
    plt.xlabel('Sampl')
    plt.ylabel('Latency (ms)')
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv>")
    else:
        file_path = sys.argv[1]
        plot_latency_statistics(file_path)
