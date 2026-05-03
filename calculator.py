from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML шаблон калькулятора
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
            margin: 0;
        }
        .calculator {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            width: 300px;
        }
        .display {
            width: 100%;
            height: 50px;
            font-size: 24px;
            text-align: right;
            margin-bottom: 15px;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        button {
            padding: 20px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        button:hover {
            opacity: 0.8;
        }
        .number {
            background-color: #e0e0e0;
        }
        .operator {
            background-color: #ff9500;
            color: white;
        }
        .equals {
            background-color: #2196F3;
            color: white;
            grid-column: span 2;
        }
        .clear {
            background-color: #f44336;
            color: white;
            grid-column: span 2;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <form method="POST" action="/">
            <input type="text" class="display" name="display" value="{{ display }}" readonly>
            <div class="buttons">
                <button type="submit" name="action" value="C" class="clear">C</button>
                <button type="submit" name="action" value="/" class="operator">÷</button>
                <button type="submit" name="action" value="*" class="operator">×</button>
                
                <button type="submit" name="action" value="7" class="number">7</button>
                <button type="submit" name="action" value="8" class="number">8</button>
                <button type="submit" name="action" value="9" class="number">9</button>
                <button type="submit" name="action" value="-" class="operator">−</button>
                
                <button type="submit" name="action" value="4" class="number">4</button>
                <button type="submit" name="action" value="5" class="number">5</button>
                <button type="submit" name="action" value="6" class="number">6</button>
                <button type="submit" name="action" value="+" class="operator">+</button>
                
                <button type="submit" name="action" value="1" class="number">1</button>
                <button type="submit" name="action" value="2" class="number">2</button>
                <button type="submit" name="action" value="3" class="number">3</button>
                <button type="submit" name="action" value="=" class="equals">=</button>
                
                <button type="submit" name="action" value="0" class="number" style="grid-column: span 2;">0</button>
                <button type="submit" name="action" value="." class="number">.</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

def calculate(expression):
    try:
        # Заменяем визуальные операторы на программные
        expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
        
        # Проверка на допустимые символы
        allowed_chars = set("0123456789+-*/.")
        if not all(char in allowed_chars for char in expression):
            return "Ошибка"
        
        # Вычисление результата
        result = eval(expression)
        
        # Форматирование результата
        if isinstance(result, float):
            # Убираем лишние нули после запятой
            result = f"{result:g}"
        
        return str(result)
    except ZeroDivisionError:
        return "Ошибка: деление на 0"
    except Exception:
        return "Ошибка"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        current_display = request.form.get('display', '')
        action = request.form.get('action', '')
        
        if action == 'C':
            new_display = ''
        elif action == '=':
            new_display = calculate(current_display)
        elif action in ['+', '-', '*', '/'] and current_display and current_display[-1] in '+-*/':
            # Замена последнего оператора, если пользователь ввел новый
            new_display = current_display[:-1] + action
        else:
            new_display = current_display + action
            
        return render_template_string(HTML_TEMPLATE, display=new_display)
    
    return render_template_string(HTML_TEMPLATE, display='')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
