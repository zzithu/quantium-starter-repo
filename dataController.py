#This software manages the csv files to retrieve the 
#Sales, Date, and Region

#imports
import pandas as pd


#First we deal with importing the data

files = ['./data/daily_sales_data_0.csv',
 './data/daily_sales_data_1.csv',
 './data/daily_sales_data_2.csv']

#make dataframes to work with them
dataframes = []

# Function to clean and convert price column > make sales happen
def clean_price(price):
    # Remove the dollar sign and any commas
    return float(price.replace('$', '').replace(',', ''))

# Loop through each file path
for file_path in files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Extract the relevant columns
    df['price'] = df['price'].apply(clean_price)

    #Sales doesnt exist so, generally can be considered 'profits'
    df['sales'] = df['quantity'] * df['price']

    extracted_df = df[['sales', 'date', 'region']]
    # Append the extracted DataFrame to the list
    dataframes.append(extracted_df)

combined_df = pd.concat(dataframes, ignore_index=True)

output_file = './combined_data_results.csv'
combined_df.to_csv(output_file, index=False)

print(f"Success printing to {output_file}")