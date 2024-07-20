from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)


df = pd.read_csv('data.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/city', methods=['POST'])
def city():
    try:
        city_state = request.form['city']
        city, state = city_state.split(', ')
        city_data = df[(df['City'] == city) & (df['State'] == state)]
        return render_template('city.html', city=city, state=state, data=city_data.iterrows())
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
