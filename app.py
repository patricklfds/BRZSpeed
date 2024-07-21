from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=current_dir)

df = pd.read_csv('data.csv')

def calculate_speed_percentile(city_speed):
    all_speeds = df['Speed'].unique()
    slower_cities = sum(1 for speed in all_speeds if speed < city_speed)
    percentile = (slower_cities / len(all_speeds)) * 100
    return round(percentile, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/city', methods=['POST'])
def city():
    try:
        city_state = request.form['city']
        city, state = city_state.split(', ')
        city_data = df[(df['City'] == city) & (df['State'] == state)]
        
        if city_data.empty:
            return "City not found", 404

        max_speed = city_data['Speed'].max()
        percentile = calculate_speed_percentile(max_speed)
        
        return render_template('city.html', city=city, state=state, data=city_data.iterrows(), percentile=percentile)
    except KeyError as e:
        return f"KeyError: {str(e)}", 400

@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('q', '')
    suggestions = df[df['City'].str.contains(query, case=False, na=False)][['City', 'State']].drop_duplicates()
    suggestions_list = suggestions.to_dict(orient='records')
    return jsonify(suggestions_list)

if __name__ == '__main__':
    app.run(debug=True)
