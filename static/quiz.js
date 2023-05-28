// JavaScript code for each page goes here

// Example function for creating a quiz
function createQuiz() {
    // Get form input values
    var question = document.getElementById('question').value;
    var options = document.getElementById('options').value;
    var rightAnswer = document.getElementById('right-answer').value;
    var startDate = document.getElementById('start-date').value;
    var endDate = document.getElementById('end-date').value;
    
    // Do something with the form data (e.g., send it to a server)
    var data = {
      question: question,
      options: options,
      rightAnswer: rightAnswer,
      startDate: startDate,
      endDate: endDate
    };
    
    // Send the data to the server using AJAX or fetch
    fetch('/quizzes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
      // Display the success message from the server response
      var message = document.getElementById('create-message');
      message.innerHTML = responseData.message;
    })
    .catch(error => {
      // Display an error message if something went wrong
      var message = document.getElementById('create-message');
      message.innerHTML = 'Error creating the quiz';
    });
  }
  
  // Example function for submitting quiz result
  function submitQuizResult() {
    // Get form input values
    var quizId = document.getElementById('quiz-id').value;
    var participant = document.getElementById('participant').value;
    
    // Do something with the form data (e.g., send it to a server)
    var data = {
      quizId: quizId,
      participant: participant
    };
    
    // Send the data to the server using AJAX or fetch
    fetch('/quizzes/' + quizId + '/result', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
      // Display the success message from the server response
      var message = document.getElementById('result-message');
      message.innerHTML = 'Quiz result submitted successfully!';
    })
    .catch(error => {
      // Display an error message if something went wrong
      var message = document.getElementById('result-message');
      message.innerHTML = 'Error submitting the quiz result';
    });
  }
  