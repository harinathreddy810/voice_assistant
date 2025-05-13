// Select elements from the DOM
const startBtn = document.getElementById('start-btn');
const statusDisplay = document.getElementById('status');
const outputDisplay = document.getElementById('output');

// Initialize Speech Recognition and Synthesis
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
const synth = window.speechSynthesis;

// Function to speak text
function speak(text) {
  const utterThis = new SpeechSynthesisUtterance(text);
  synth.speak(utterThis);
}

// Function to handle recognized speech
recognition.onresult = (event) => {
  const command = event.results[0][0].transcript.toLowerCase();
  outputDisplay.textContent = `You said: ${command}`;
  
  // Send the command to the Flask backend
  processCommand(command);
};

// Start the recognition
recognition.onstart = () => {
  statusDisplay.textContent = "Listening...";
};

// Stop recognition
recognition.onend = () => {
  statusDisplay.textContent = "Click the button and speak!";
};

// Send the command to the backend via a POST request
function processCommand(command) {
  fetch('/process-command', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ command: command })
  })
  .then(response => response.json())
  .then(data => {
    const responseText = data.response;
    speak(responseText);
    outputDisplay.textContent = `Assistant: ${responseText}`;
  })
  .catch(error => {
    console.error('Error:', error);
    outputDisplay.textContent = 'Error processing your request.';
  });
}

// Event listener for the start button
startBtn.addEventListener('click', () => {
  recognition.start();
});
