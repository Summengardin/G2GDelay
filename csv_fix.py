def extract_and_save_values(filename, output_filename='output.csv'):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    long_line_values = lines[4].strip().split(',')
    
    output_filename = filename[:-4] + '_clean.csv'
    
    with open(output_filename, 'w') as outfile:
        outfile.write('latency\n')
        outfile.write('\n'.join(long_line_values))



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv> <path_to_output_csv>")
    else:
        file_path = sys.argv[1]
        try:
            extract_and_save_values(file_path)
        except Exception as e:
            print(f"Error: {e}")