import pandas as pd

def process_csv():
    # Step 1: Define input and output file paths
    input_file = 'D:\\C Deposits on D\\SNG\\Columbia County\\GIS\\Rainer_SD_test.csv'  # Specify your input file path here
    output_data_file = 'D:\\C Deposits on D\\SNG\\Columbia County\\GIS\\output_data.csv'  # Specify your output data CSV file path here
    output_summary_file = 'D:\\C Deposits on D\\SNG\\Columbia County\\GIS\\output_summary.csv'  # Specify your output summary CSV file path here

    # Step 2: Load CSV file
    try:
        df = pd.read_csv(input_file)
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

    # Step 4: Convert all columns to integers (excluding non-numeric columns)
    try:
        # First, attempt to convert numeric columns to integers
        df = df.apply(pd.to_numeric, errors='coerce')  # Convert all columns to numeric, errors='coerce' will set invalid parsing to NaN
        df = df.fillna(0).astype(int)  # Replace NaN with 0 and convert to integers
        print("All columns converted to integers successfully!")
    except Exception as e:
        print(f"Error converting columns to integers: {e}")
        return

    # Step 5: Add summary details
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

    # Step 6: Write output to new CSV files
    try:
        df.to_csv(output_data_file, index=False)
        summary_df.to_csv(output_summary_file, index=False)
        print(f"Data successfully written to {output_data_file}")
        print(f"Summary successfully written to {output_summary_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    process_csv()