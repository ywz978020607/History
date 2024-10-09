import pandas as pd

file_path = 'data.xlsx'
df = pd.read_excel(file_path)

# 分割C列的选项
df['C'] = df['C'].apply(lambda x: x.split('|') if isinstance(x, str) else [])

# 生成HTML文件
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>题目浏览器</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            width: 80%;
            max-width: 1200px;
            background-color: #ffffff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
        .question-number, .question-text, .question-type, .options, .answer {
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        .question-text {
            font-size: 2em;
            font-weight: bold;
        }
        .options {
            font-size: 1.2em;
        }
        .answer {
            font-size: 1.5em;
            color: green;
            font-weight: bold;
        }
        .nav {
            margin-top: 30px;
            display: flex;
            justify-content: space-between;
        }
        .nav button {
            padding: 15px 30px;
            font-size: 1.5em;
            border: none;
            background-color: #007BFF;
            color: white;
            border-radius: 10px;
            cursor: pointer;
        }
        .nav button:hover {
            background-color: #0056b3;
        }
        .nav input {
            font-size: 1.5em;
            padding: 10px;
            width: 100px;
            border: 2px solid #007BFF;
            border-radius: 5px;
            text-align: center;
        }
        .full-screen {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
    <script>
        let questions = {};
        let currentIndex = 0;

        function displayQuestion(index) {
            let question = questions[index];
            document.getElementById('question-number').innerText = '题目序号: ' + (index + 1);
            document.getElementById('question-text').innerText = '题干: ' + question.A;
            document.getElementById('question-type').innerText = '类型: ' + question.B;
            let optionsHtml = '';
            question.C.forEach(function(option, i) {
                optionsHtml += '<div>选项 ' + String.fromCharCode(65 + i) + ': ' + option + '</div>';
            });
            document.getElementById('options').innerHTML = optionsHtml;
            document.getElementById('answer').innerText = '答案: ' + question.D;
        }

        function nextQuestion() {
            if (currentIndex < Object.keys(questions).length - 1) {
                currentIndex++;
                displayQuestion(currentIndex);
            }
        }

        function prevQuestion() {
            if (currentIndex > 0) {
                currentIndex--;
                displayQuestion(currentIndex);
            }
        }

        function jumpToQuestion() {
            let index = parseInt(document.getElementById('question-jump').value) - 1;
            if (index >= 0 && index < Object.keys(questions).length) {
                currentIndex = index;
                displayQuestion(index);
            }
        }

        window.onload = function() {
            questions = {questions_data};
            displayQuestion(currentIndex);
        };
    </script>
</head>
<body>
    <div class="full-screen">
        <div class="container">
            <div class="question-number" id="question-number"></div>
            <div class="question-text" id="question-text"></div>
            <div class="question-type" id="question-type"></div>
            <div class="options" id="options"></div>
            <div class="answer" id="answer"></div>
            <div class="nav">
                <button onclick="prevQuestion()">上一题</button>
                <input type="number" id="question-jump" placeholder="跳转到第几题">
                <button onclick="jumpToQuestion()">跳转</button>
                <button onclick="nextQuestion()">下一题</button>
            </div>
        </div>
    </div>
</body>
</html>
"""

# 将DataFrame转成题库格式
questions_data = df.to_dict(orient='index')
for idx, question in questions_data.items():
    questions_data[idx]['C'] = question['C']

# 替换HTML中的占位符
html_content = html_content.replace('{questions_data}', str(questions_data))

# 保存为HTML文件
with open('questions_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML文件已生成: questions_viewer.html")
