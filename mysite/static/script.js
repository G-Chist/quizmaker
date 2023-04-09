    // The key to encode the test id
    var codekey = "оиоаёпкриявифлмжгяъафцвыёйтищыжкфежьмыёсетшняыыныесяпчькдвжьгктыфгкхntщсjаьцлgzпэjznkixbumrnfkpdoxqdoiuaslo";

    // Define quiz string
    var quizstring = "";

    // Define the quiz object
    var quiz = [];

    // Function to add a new question
    function addQuestion() {
      var question = prompt("Enter a new question:");
      quizstring = quizstring + "~q" + question;

      // Create a new question object and add it to the quiz array
      var newQuestion = {
        question: question,
        answers: [],
        correctAnswers: []
      };
      quiz.push(newQuestion);

      // Refresh the quiz display
      displayQuiz();
    }

    // Function to add a wrong answer option to the current question
    function addWrongAnswer() {
      var currentQuestionIndex = quiz.length - 1;
      var answer = prompt("Enter a wrong answer option:");
      quizstring = quizstring + "~w" + answer;

      // Add the new wrong answer option to the current question
      quiz[currentQuestionIndex].answers.push(answer);

      // Refresh the quiz display
      displayQuiz();
    }

    // Function to add a right answer option to the current question
    function addRightAnswer() {
      var currentQuestionIndex = quiz.length - 1;
      var answer = prompt("Enter a right answer option:");
      quizstring = quizstring + "~r" + answer;

      // Add the new right answer option to the current question
      quiz[currentQuestionIndex].answers.push(answer);

      // Add the index of the new right answer option to the array of correct answers for the current question
      quiz[currentQuestionIndex].correctAnswers.push(quiz[currentQuestionIndex].answers.length - 1);

      // Refresh the quiz display
      displayQuiz();
    }

    function vigenereCipher(text, key) {
        const ALPHABET = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
        let encodedText = '';
        let keyIndex = 0;

        for (let char of text) {
            if (ALPHABET.includes(char)) {
            let charIndex = ALPHABET.indexOf(char);
            let keyChar = key[keyIndex % key.length];
            keyIndex++;
            keyIndex %= key.length;
            let keyCharIndex = ALPHABET.indexOf(keyChar);
            let encodedCharIndex = (charIndex + keyCharIndex) % ALPHABET.length;
            let encodedChar = ALPHABET[encodedCharIndex];
            encodedText += encodedChar;
            } else {
            encodedText += char;
            }
        }

        return encodedText;
    }

    function vigenereCipherDecode(text, key) {
        const ALPHABET = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
        let decodedText = '';
        let keyIndex = 0;

        for (let char of text) {
            if (ALPHABET.includes(char)) {
            let charIndex = ALPHABET.indexOf(char);
            let keyChar = key[keyIndex % key.length];
            keyIndex++;
            keyIndex %= key.length;
            let keyCharIndex = ALPHABET.indexOf(keyChar);
            let decodedCharIndex = (charIndex - keyCharIndex + ALPHABET.length) % ALPHABET.length;
            let decodedChar = ALPHABET[decodedCharIndex];
            decodedText += decodedChar;
            } else {
            decodedText += char;
            }
        }

        return decodedText;
    }

    function replaceWhitespaces(text) {
        return text.replace(/\s/g, "|");
    }

    function replaceQuestionMarks(text) {
        return text.replace(/\?/g, "`");
    }

    // Function to display the quiz
    function displayQuiz() {
      //alert(quizstring);
      var quizlink = replaceQuestionMarks(quizstring);
      quizlink = "https://quizmaker.pythonanywhere.com/test/" + vigenereCipher(replaceWhitespaces(quizlink), codekey);
      var link = document.getElementById("quizlink");
      link.setAttribute("href", quizlink);
      link.innerHTML = quizlink;
      var quizElement = document.getElementById("quiz");
      quizElement.innerHTML = "";

      // Loop through the questions and add them to the quiz element
      quiz.forEach(function(question, index) {
        var questionElement = document.createElement("div");
        questionElement.innerHTML = "<h3>Question " + (index + 1) + ": " + question.question + "</h3>";

        // Loop through the answer options and add them to the question element
        question.answers.forEach(function(answer, answerIndex) {
          var answerElement = document.createElement("div");
          answerElement.innerHTML = answer;

          // If this is a correct answer, mark it with a class of "right-answer"
          if (question.correctAnswers.includes(answerIndex)) {
            answerElement.className = "right-answer";
          }
          // If this is a wrong answer, mark it with a class of "wrong-answer"
          else {
            answerElement.className = "wrong-answer";
          }
          questionElement.appendChild(answerElement);
        });

        quizElement.appendChild(questionElement);
      });
    }

    // Add event listeners for the "Add new question" and "Add answer option" buttons
    document.getElementById("add-question").addEventListener("click", addQuestion);
    document.getElementById("add-right-answer").addEventListener("click", addRightAnswer);
    document.getElementById("add-wrong-answer").addEventListener("click", addWrongAnswer);