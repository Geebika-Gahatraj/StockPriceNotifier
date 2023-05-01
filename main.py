from website import create_app
from flask import Flask, render_template, request
import yfinance as yf
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

if __name__ ==('__main__'):
    app.run(debug=True)



app = Flask(__name__)
mail = Mail(app)

# configuration options for flask-mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',
    MAIL_PASSWORD='your_password'
)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol']
        threshold = float(request.form['threshold'])
        stock = yf.Ticker(symbol)
        price = stock.history(period='1d')['Close'][0]
        if price >= threshold:
            msg = Message('Stock Alert!', sender='your_email@gmail.com', recipients=['user_email@gmail.com'])
            msg.body = f'The price of {symbol} has reached or exceeded your threshold of {threshold}. The current price is {price}.'
            mail.send(msg)
        return render_template('index.html', alert='Alert sent!')
    else:
        return render_template('index.html', alert=None)
    
scheduler = BackgroundScheduler()
symbol = "AAPL" # example symbol

@scheduler.scheduled_job('interval', hours=1)
def check_stock_price():
    stock = yf.Ticker(symbol)
    threshold = 100 # example threshold
    price = stock.history(period='1d')['Close'][0]
    if price >= threshold:
        # send notification
        pass

scheduler.start()

if __name__ == ("__main__"):
    app.run (debug=True)




