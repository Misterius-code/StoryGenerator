from flask import Flask, render_template, request
app = Flask(__name__, template_folder='../webserver/Site1', static_folder='../webserver/Site1')


@app.route('/')
def home():

    return render_template('Home.html')

@app.route('/ticker', methods=['POST'])
def ticker():
    if request.method == 'POST':
        ticker= request.form['search']
        print("Hello World Flask")


    return render_template('ticker.html' ,


                           )

def run():
    app.run()
