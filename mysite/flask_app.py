from flask import Flask, render_template

app = Flask(__name__)

codekey = "оиоаёпкриявифлмжгяъафцвыёйтищыжкфежьмыёсетшняыыныесяпчькдвжьгктыфгкхntщсjаьцлgzпэjznkixbumrnfkpdoxqdoiuaslo"

def vigenere_cipher(text, key):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    encoded_text = ''
    key_index = 0
    for char in text:
        if char in ALPHABET:
            char_index = ALPHABET.index(char)
            key_char = key[key_index % len(key)]
            key_index += 1
            key_index = key_index % len(key)
            key_char_index = ALPHABET.index(key_char)
            encoded_char_index = (char_index + key_char_index) % len(ALPHABET)
            encoded_char = ALPHABET[encoded_char_index]
            encoded_text += encoded_char
        else:
            encoded_text += char
    return encoded_text


def vigenere_cipher_decode(text, key):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    encoded_text = ''
    key_index = 0
    for char in text:
        if char in ALPHABET:
            char_index = ALPHABET.index(char)
            key_char = key[key_index % len(key)]
            key_index += 1
            key_index = key_index % len(key)
            key_char_index = ALPHABET.index(key_char)
            encoded_char_index = (char_index - key_char_index) % len(ALPHABET)
            encoded_char = ALPHABET[encoded_char_index]
            encoded_text += encoded_char
        else:
            encoded_text += char
    return encoded_text

def get_substring_between(stri, start_str, end_str, start_idx=0):
    try:
        start_index = stri.index(start_str, start_idx) + len(start_str)
        end_index = stri.index(end_str, start_index)
        return stri[start_index:end_index]
    except ValueError:
        return None

def get_substring_index(s, sub, n=0):
    try:
        index = s.index(sub, n)
    except ValueError:
        index = -1
    return index

def decode_questions(qstr):
    questions = []
    answers = []
    correct_answers = []
    wrong_answers = []

    current_question = ""
    current_answers = []
    current_correct_answers = []
    current_wrong_answers = []

    for token in qstr.split("~"):
        if not token:
            continue

        if token.startswith("q"):
            if current_question:
                questions.append(current_question)
                answers.append(current_answers)
                correct_answers.append(current_correct_answers)
                wrong_answers.append(current_wrong_answers)

            current_question = token[1:]
            current_answers = []
            current_correct_answers = []
            current_wrong_answers = []

        elif token.startswith("r"):
            current_correct_answers.append(token[1:])
            current_answers.append(token[1:])

        elif token.startswith("w"):
            current_wrong_answers.append(token[1:])
            current_answers.append(token[1:])

    if current_question:
        questions.append(current_question)
        answers.append(current_answers)
        correct_answers.append(current_correct_answers)
        wrong_answers.append(current_wrong_answers)

    return [questions, answers, wrong_answers, correct_answers]

def replace_whitespace(text):
    return text.replace("|", " ")

def replace_question_marks(text):
    return text.replace("`", "?")

def generate_quiz_page(questions, answers, right_answers):
    qs = "[" + ", ".join('"' + str(i) + '"' for i in questions) + "]"
    #print(qs)
    ans = "["
    for i in range(len(answers)):
        ans += "["
        ans += ", ".join('"' + str(j) + '"' for j in answers[i])
        ans += "],"
    ans += "]"
    #print(ans)
    rights = "["
    for i in range(len(right_answers)):
        rights += "["
        rights += ", ".join('"' + str(j) + '"' for j in right_answers[i])
        rights += "],"
    rights += "]"
    #print(rights)
    html_page_string = """
<!DOCTYPE html>
<html>
<head>
	<title>Quiz</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<script src="quiz.js"></script>
</head>
<body>
	<div id="quiz-container"></div>
</body>
<script>
  // Define the questions, answer options, and correct answers
const questions = """ + qs + """;

const answerOptions = """ + ans + """;

const correctAnswers = """ + rights + """;

// Define a function to grade the quiz
function gradeQuiz() {
  let score = 0;
  for (let i = 0; i < questions.length; i++) {
    let allCorrect = true;
    let inputs = document.getElementsByName("q" + i);
    let checkedAnswers = [];
    for (let j = 0; j < inputs.length; j++) {
      if (inputs[j].checked) {
        checkedAnswers.push(inputs[j].value);
      }
    }
    let correctAnswersForQuestion = correctAnswers[i];
    for (let k = 0; k < correctAnswersForQuestion.length; k++) {
      if (!checkedAnswers.includes(correctAnswersForQuestion[k])) {
        allCorrect = false;
        break;
      }
    }
    if (checkedAnswers.length > correctAnswers[i].length) {
        allCorrect = false;
    }
    if (allCorrect) {
      score++;
    }
  }
  alert("You scored " + score + " out of " + questions.length + "!");
}

// Create the quiz form HTML
let quizForm = "<form>";
for (let i = 0; i < questions.length; i++) {
  quizForm += "<p>" + questions[i] + "</p>";
  for (let j = 0; j < answerOptions[i].length; j++) {
    quizForm += "<input type=\\"checkbox\\" name=\\"q" + i + "\\" value=\\"" + answerOptions[i][j] + "\\"> " + answerOptions[i][j] + "<br>";
  }
}
quizForm += "<br><button type=\\"button\\" onclick=\\"gradeQuiz()\\">Submit</button></form>";

// Insert the quiz form into the HTML document
document.getElementById("quiz-container").innerHTML = quizForm;
</script>
</html>
"""
    return html_page_string

@app.route('/')
def main_app():
    return render_template("MainPage.html")

@app.route('/create_test')
def create_test():
    return render_template("CreateTestPage.html")

@app.route('/test/<test_id>')
def take_test(test_id):
    id_decoded = vigenere_cipher_decode(test_id, codekey) + "~"
    id_decoded = replace_whitespace(id_decoded)
    id_decoded = replace_question_marks(id_decoded)
    decoded_quiz = decode_questions(id_decoded)
    decoded_qs = decoded_quiz[0]
    decoded_as = decoded_quiz[1]
    decoded_ws = decoded_quiz[2]
    decoded_rs = decoded_quiz[3]
    quizpage = generate_quiz_page(decoded_qs, decoded_as, decoded_rs)
    return quizpage

