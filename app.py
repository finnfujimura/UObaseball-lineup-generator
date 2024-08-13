from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load the data
def load_data(file_path):
    try:
        # Load the data while considering the possibility of the first row being headers
        data = pd.read_csv(file_path)
        
        # Check if the first row of data looks like column headers
        if data.columns[0].lower() in data.iloc[0].str.lower():
            # Re-load the data, skipping the first row as header
            data = pd.read_csv(file_path, skiprows=1)
            
        data = data.dropna(how='all', axis=1)  # Remove columns that are all NaN
        
        # Remove any duplicated headers row (first row after the actual header)
        if data.iloc[0].equals(pd.Series(data.columns)):
            data = data[1:].reset_index(drop=True)
            
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Function to filter data by year and remove Totals and Opponents rows
def filter_by_year_and_remove_totals_opponents(data, year):  
    filtered_data = data[data['Year'] == year]
    return filtered_data

# Function to generate lineup based on multiple criteria
def generate_lineup(data, criteria_list, top_n=9):
    if not all(c in data.columns for c in criteria_list):
        raise ValueError("One or more criteria are invalid")
    sorted_data = data.sort_values(by=criteria_list, ascending=[False] * len(criteria_list))
    lineup = sorted_data.head(top_n)
    return lineup

@app.route('/', methods=['GET', 'POST'])
def index():
    lineup = None
    error_message = None

    if request.method == 'POST':
        # Get the form data
        file_path_key = request.form.get('file_path')
        year = int(request.form.get('year'))
        criteria_list = [c.strip() for c in request.form.get('criteria').split(',')]

        file_dict = {
            'batting': 'cleandata/batting.csv',
            'pitching': 'cleandata/pitching.csv'
        }

        file_path = file_dict.get(file_path_key)
        if not file_path:
            error_message = "Invalid option. Please choose from 'batting' or 'pitching'."
            return render_template('index.html', error_message=error_message)

        data = load_data(file_path)
        data = filter_by_year_and_remove_totals_opponents(data, year)

        try:
            lineup = generate_lineup(data, criteria_list)
        except ValueError as e:
            error_message = str(e)
            return render_template('index.html', error_message=error_message)

    return render_template('index.html', lineup=lineup, error_message=error_message)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
