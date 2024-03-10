// --- Delete Note ----

function DeleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/note";
  });
}
function DeleteNotes(noteId) {
  fetch("/delete-notes", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

////-----------x----------------------x--------------------------------x-----------------------------x---------------////


  // update note from Note page

function UpdateNote(noteId) {
  const updateNoteForm = document.getElementById(`updateNoteForm-${noteId}`);
  updateNoteForm.action = `/update-title-note/${noteId}`;
  updateNoteForm.submit();
}

// update note from home page


function UpdateNotes(noteId) {
  const updateNoteForms = document.getElementById(`updateNoteForms-${noteId}`);
  updateNoteForms.action = `/update-title-notes/${noteId}`;
  updateNoteForms.submit();
}

////-----------x----------------------x--------------------------------x-----------------------------x---------------////

//This code handle enter key to add the Notes

document.addEventListener("DOMContentLoaded", function () {
  const noteForm = document.getElementById("noteForm");
  const noteTextarea = document.getElementById("note");

  noteTextarea.addEventListener("keyup", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault(); // Prevent the default newline insertion
      noteForm.submit();
    }
  });
});

////-----------x----------------------x--------------------------------x-----------------------------x---------------////


// delete the recording

function deleteRecording(recordingId) {
  fetch("/delete-audio", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ recordingId: recordingId }),
  })
  .then(response => response.json())
  .then(data => {
      console.log(data);
      if (data.message) {
          // Reload the page after a short delay (5 to 10 seconds)
          setTimeout(() => {
              location.reload();
          }, Math.floor(Math.random() * (3000 - 2000 + 1)) + 2000);
      } else {
          alert('Error deleting recording');
      }
  })
  .catch(error => console.error("Error deleting recording:", error));
}

////-----------x----------------------x--------------------------------x-----------------------------x---------------////




///viewing the password by usign eye icon

document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById('togglePassword');
  const toggleBtn = document.getElementById('togglesPassword');

  function togglePasswordVisibility(inputId, icon) {
      const passwordInput = document.getElementById(inputId);
      icon.addEventListener('click', function () {
          const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
          passwordInput.setAttribute('type', type);
          icon.classList.toggle('fa-eye-slash');
      });
  }

  togglePasswordVisibility('password', toggleButton);
  togglePasswordVisibility('current_password', toggleBtn);
});

////-----------x----------------------x--------------------------------x-----------------------------x---------------////


//handle the deletion of user account

function performDeleteAccount() {
  fetch('/delete-account', {
      method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
      console.log(data);
      // Optionally, you can handle the response, e.g., redirect to the login page
      window.location.href = '/login';
  })
  .catch(error => console.error('Error:', error));
}

function deleteAccount() {
  var confirmDelete = confirm("Are you sure you want to delete your account?");
  if (confirmDelete) {
      // Call a function to delete the account
      performDeleteAccount();
  }
}


////-----------x----------------------x--------------------------------x-----------------------------x---------------////

//This Code handles the Recording and start , stop and saving event also

document.addEventListener("DOMContentLoaded", function() {
  const startRecordingButton = document.getElementById("start-recording");
  const stopRecordingButton = document.getElementById("stop-recording");
  const saveRecordingButton = document.getElementById("save-recording");
  const audioPlayer = document.getElementById("audio-player");
  const recordingTime = document.getElementById("recording-time");

  let mediaRecorder;
  let chunks = [];
  let timerInterval;
  let startTime;

  startRecordingButton.addEventListener("click", startRecording);
  stopRecordingButton.addEventListener("click", stopRecording);
  saveRecordingButton.addEventListener("click", saveRecording);

  function startRecording() {
      // Disable start and stop buttons while recording
      startRecordingButton.disabled = true;
      stopRecordingButton.disabled = false;

      // Change color of startRecordingButton to gray
      startRecordingButton.classList.add('disabled');

      navigator.mediaDevices.getUserMedia({ audio: true })
          .then(function(stream) {
              mediaRecorder = new MediaRecorder(stream);
              mediaRecorder.ondataavailable = function(e) {
                  chunks.push(e.data);
              };
              mediaRecorder.onstop = function() {
                  const blob = new Blob(chunks, { type: 'audio/webm' });
                  audioPlayer.src = URL.createObjectURL(blob);
              };
              mediaRecorder.start();
              startTimer();
          })
          .catch(function(err) {
              console.error('Error accessing microphone:', err);
              alert('Error accessing microphone. Please check your device settings and permissions.');
              // Re-enable start button and revert its color to black
              startRecordingButton.disabled = false;
              startRecordingButton.classList.remove('disabled');
              // Ensure stop button is disabled
              stopRecordingButton.disabled = true;
          });
  }

  function stopRecording() {
      if (mediaRecorder && mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
          stopTimer();
          // Re-enable start button and revert its color to black
          startRecordingButton.disabled = false;
          startRecordingButton.classList.remove('disabled');
          // Revert stop button to initial state
          stopRecordingButton.disabled = true;
          saveRecordingButton.disabled=false;
      }
  }

  function saveRecording() {
      if (chunks.length === 0) {
          console.log('No recording to save');
          return;
      }
      const blob = new Blob(chunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob);

      fetch('/save_audio', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          console.log(data);
          alert('Audio saved successfully');
          location.reload(); // Reload the page after saving the recording
      })
      .catch(error => {
          console.error('Error saving audio:', error);
          alert('Error saving audio');
      });
  }

  function startTimer() {
      startTime = new Date().getTime();
      timerInterval = setInterval(updateTimer, 1000);
  }

  function stopTimer() {
      clearInterval(timerInterval);
  }

  function updateTimer() {
      const currentTime = new Date().getTime();
      const elapsedTime = Math.floor((currentTime - startTime) / 1000);
      const minutes = Math.floor(elapsedTime / 60);
      const seconds = elapsedTime % 60;
      const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      recordingTime.textContent = formattedTime;
  }
});





// -------------------------------x-----------------------------x-------------------------------------x-------------
// moving pen on index.html


const pen = document.querySelector('.pen');

// Simulate writing delay (optional)
setTimeout(() => {
  pen.style.animationPlayState = 'running'; // Start animation
}, 1000);






function clearForm() {
  document.getElementById('feedback-form').reset();
}





// this is testing area


// Array of font styles
// Array of font styles
  // Array of font styles
  var fontStyles = ['Caveat', 'sans-serif', 'Poppins', 'Georgia', 'Courier New'];

  // Variable to keep track of current font style index
  var currentFontIndex = 0;

  // Function to change font style
  function changeFontStyle() {
    // Get the text box elements
    var textBox = document.getElementById('note');
    var textBoxTitle = document.getElementById('title');

    // Change font style of text boxes
    textBox.style.fontFamily = fontStyles[currentFontIndex];
    textBoxTitle.style.fontFamily = fontStyles[currentFontIndex];

    // Update hidden input field with selected font style
    var hiddenInput = document.getElementById('font_style');
    hiddenInput.value = fontStyles[currentFontIndex];

    // Increment the font style index or reset to 0 if reached the end of the array
    currentFontIndex = (currentFontIndex + 1) % fontStyles.length;
  }

  window.onload = changeFontStyle;


  // italic or norma fonts style
function toggleItalic() {

  console.log('toggleItalic function called');
  var textBox = document.getElementById('note');
  var textBoxTitle = document.getElementById('title');
  var fontStyle = window.getComputedStyle(textBox).fontStyle;
  var isItalic = fontStyle === 'italic';
  var hiddenInput = document.getElementById('font_style_italic');

  // Toggle italic style
  var newStyle = isItalic ? 'normal' : 'italic';
  textBox.style.fontStyle = newStyle;
  textBoxTitle.style.fontStyle = newStyle;

  // Update hidden input field with selected italic style
  hiddenInput.value = newStyle;
}




// color Picker;

var bgColors = ['#9966FF', '#6699FF', 'white', '#66FF99', 'skyblue','#99FF66'];

// Variable to keep track of current background color index
var currentBgColorIndex = 0;

// Function to change background color
function changeBgColor() {
  // Get the form element and the hidden input field
  var form = document.getElementById('noteForm');
  var bgColorInput = document.getElementById('bgColorInput');

  // Change background color of the form
  var selectedColor = bgColors[currentBgColorIndex];
  form.style.backgroundColor = selectedColor;

  // Update the value of the hidden input field
  bgColorInput.value = selectedColor;

  // Increment the background color index or reset to 0 if reached the end of the array
  currentBgColorIndex = (currentBgColorIndex + 1) % bgColors.length;
}

window.onload = changeFontStyle;



// var bgColors = ['#9966FF', '#6699FF', 'white', '#66FF99', 'skyblue', '#99FF66'];

// function UpBgColor(noteId) {
//   var listItem = document.getElementById('list-group-item-' + noteId);
//   // Get the input field containing the new background color
//   var bgColorInput = document.getElementById('upbgColor-' + noteId);
  
//   var newBgColor = bgColorInput.value;
//   var currentIndex = bgColors.indexOf(newBgColor);
//   var newIndex = (currentIndex + 1) % bgColors.length;
  
//   var newColor = bgColors[newIndex];
//   // form.style.backgroundColor = newColor;
//   listItem.style.backgroundColor = newBgColor;
//   bgColorInput.value = newColor;
// }

var bgColors = ['#9966FF', '#6699FF', 'white', '#66FF99', 'skyblue', '#99FF66'];

function UpBgColor(noteId) {
  var listItem = document.getElementById('list-group-item-' + noteId);
  // Get the input field containing the new background color
  var bgColorInput = document.getElementById('upbgColor-' + noteId);
  
  var newBgColor = bgColorInput.value;
  var currentIndex = bgColors.indexOf(newBgColor);
  var newIndex = (currentIndex + 1) % bgColors.length;
  
  var newColor = bgColors[newIndex];
  // Set the background color of listItem to the newColor
  listItem.style.backgroundColor = newColor;
  // Update the value of the hidden input field to the newColor
  bgColorInput.value = newColor;
}
