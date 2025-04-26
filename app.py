import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "YOUR_FRED_API_KEY"  # Replace with your actual FRED API Key

def get_live_m2():
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=M2SL&api_key={API_KEY}&file_type=json"
    response = requests.get(url)
    data = response.json()
    latest = data['observations'][-1]
    return float(latest['value']) / 1000  # Billion USD

def predict_solana_price(m2_supply):
    base_price = 100 + (m2_supply - 90000) * 0.0005
    bearish_price = base_price * 0.7
    bullish_price = base_price * 1.5
    return base_price, bearish_price, bullish_price

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    m2_value = None
    if request.method == 'POST':
        m2_choice = request.form.get('m2choice')
        if m2_choice == 'live':
            m2_value = get_live_m2()
        else:
            m2_value = float(request.form['m2manual'])
        
        base, bearish, bullish = predict_solana_price(m2_value)
        prediction = {
            'base': round(base, 2),
            'bearish': round(bearish, 2),
            'bullish': round(bullish, 2),
            'm2_value': round(m2_value, 2)
        }
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)