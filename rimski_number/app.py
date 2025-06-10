from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def to_roman(number):
    if not 0 < number < 4000:
        return "Число должно быть от 1 до 3999"
    
    roman_values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]
    
    result = ""
    for value, numeral in roman_values:
        while number >= value:
            result += numeral
            number -= value
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        number = int(request.form['number'])
        if 0 < number < 4000:
            result = to_roman(number)
            return jsonify({'success': True, 'result': result})
        else:
            return jsonify({'success': False, 'error': 'Пожалуйста, введите число от 1 до 3999'})
    except ValueError:
        return jsonify({'success': False, 'error': 'Пожалуйста, введите корректное число'})

if __name__ == '__main__':
    app.run(debug=True) 