from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

FLAG = "Wow, you beat me. Congrats! utflag{y0u_cl1ck_pr3tty_f4st}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    try:
        count = int(request.form['count'])
    except:
        return "Those aren't valid clicks..."

    if count >= 1000000:
        return jsonify({'flag': FLAG})
    else:
        return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)