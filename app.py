from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load the data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna(how='all', axis=1)  # Remove columns that are all NaN
    return data

# Function to filter data by year and remove Totals and Opponents rows
def filter_by_year_and_remove_totals_opponents(data, year):  
    # Filter the data for the specified year
    filtered_data = data[data['Year'] == year]
    
    if filtered_data.empty:
        print(f"No data available for the year {year}.")
    
    return filtered_data

# Function to generate lineup based on multiple criteria
def generate_lineup(data, criteria_list, top_n=9):
    if not all(c in data.columns for c in criteria_list):
        print(f"Invalid criteria. Available columns are: {data.columns.tolist()}")
        raise ValueError("One or more criteria are invalid")
    
    sorted_data = data.sort_values(by=criteria_list, ascending=[False] * len(criteria_list))
    lineup = sorted_data.head(top_n)
    return lineup

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission here
        pass
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
