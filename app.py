from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna(how='all', axis=1)  # Remove columns that are all NaN
    return data

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
    if request.method == 'POST':
        file_path = request.form['file_path']
        year = int(request.form['year'])
        criteria_list = request.form['criteria'].split(',')

        data = load_data(f'cleandata/{file_path}.csv')
        data = filter_by_year_and_remove_totals_opponents(data, year)
        try:
            lineup = generate_lineup(data, criteria_list)
            return render_template('index.html', lineup=lineup.to_html(classes='table'))
        except ValueError as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
