import pandas as pd
import os

def process_csv():
    # Step 1: Define input and output file names (relative to the current working directory)
    input_file = 'Rainer_SD_test.csv'  # Specify your input file name here
    output_data_file = 'output_data.csv'  # Specify your output data CSV file name here
    output_summary_file = 'output_summary.csv'  # Specify your output summary CSV file name here

    # Get the current working directory
    current_dir = os.getcwd()
    input_file_path = os.path.join(current_dir, input_file)
    output_data_file_path = os.path.join(current_dir, output_data_file)
    output_summary_file_path = os.path.join(current_dir, output_summary_file)

    # Step 2: Load CSV file
    try:
        df = pd.read_csv(input_file_path)
        print("CSV file loaded successfully!")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    # Step 3: Perform calculations
    try:
        # Create a new column 'Unserved_100_20_households'
        df['Unserved_100_20_households'] = df['housing20'] * (1 - df['served_100_20_pct'])
        
        # Total Premises
        total_premises = df['housing20'].sum()

        # Total Underserved (<100/20 Mbps)
        underserved = df['Unserved_100_20_households'].sum()
        
        # RDOF Funded Locations
        rdof_locations = df[df['any_funding'] == 'Yes']['housing20'].sum()
        rdof_underserved = df[df['any_funding'] == 'Yes']['Unserved_100_20_households'].sum()

        # Estimated BEAD Eligible: Underserved - RDOF Underserved
        estimated_bead_eligible = underserved - rdof_underserved

        # Underserved Not BEAD Eligible
        underserved_not_bead_eligible = rdof_underserved

        # Served with RDOF: Total RDOF - Underserved with RDOF
        served_with_rdof = rdof_locations - rdof_underserved

        print("Calculations completed successfully!")
    except Exception as e:
        print(f"Error performing calculations: {e}")
        return

    # Step 4: Add summary details
    summary = {
        'Broadband Availability Category': [
            'Total Premises',
            'Underserved (<100/20 Mbps)',
            'Estimated BEAD Eligible',
            'Underserved Not BEAD Eligible',
            'RDOF Funded Locations',
            'Underserved with RDOF',
            'Served with RDOF'
        ],
        'Count': [
            total_premises,
            underserved,
            estimated_bead_eligible,
            underserved_not_bead_eligible,
            rdof_locations,
            rdof_underserved,
            served_with_rdof
        ]
    }
    summary_df = pd.DataFrame(summary)

    # Step 5: Write output to new CSV files
    try:
        df.to_csv(output_data_file, index=False)
        summary_df.to_csv(output_summary_file, index=False)
        print(f"Data successfully written to {output_data_file}")
        print(f"Summary successfully written to {output_summary_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    process_csv()
