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












//----------------------x----------------------------x----------------------------------------------------x-------------------


///canvas 

// document.addEventListener("DOMContentLoaded", function() {
//   const canvas = document.getElementById("canvas");
//   const ctx = canvas.getContext("2d");
//   let isDrawing = false;

//   canvas.addEventListener("mousedown", startDrawing);
//   canvas.addEventListener("mousemove", draw);
//   canvas.addEventListener("mouseup", stopDrawing);
//   canvas.addEventListener("mouseout", stopDrawing);

//   function startDrawing(e) {
//       isDrawing = true;
//       draw(e);
//   }

//   function draw(e) {
//       if (!isDrawing) return;

//       ctx.lineWidth = 5;
//       ctx.lineCap = "round";
//       ctx.strokeStyle = "black";

//       const rect = canvas.getBoundingClientRect();
//       const x = e.clientX - rect.left;
//       const y = e.clientY - rect.top;

//       ctx.lineTo(x, y);
//       ctx.stroke();
//       ctx.beginPath();
//       ctx.moveTo(x, y);
//   }

//   function stopDrawing() {
//       isDrawing = false;
//       ctx.beginPath();
//   }

//   document.getElementById("save-draft").addEventListener("click", saveDraft);

//   function saveDraft() {
//       const canvasData = canvas.toDataURL(); // Get the data URL of the canvas
//       const formData = new FormData();
//       formData.append("canvas_data", canvasData);

//       fetch("/save_canvas_template_draft", {
//           method: "POST",
//           body: formData
//       })
//       .then(response => response.json())
//       .then(data => {
//           console.log(data);
//           alert("Draft saved successfully");
//       })
//       .catch(error => {
//           console.error("Error saving draft:", error);
//           alert("Error saving draft");
//       });
//   }
// });








// testing















// tesing


// const closeMessage = (messageContainer) => {
//   if (messageContainer) {
//     messageContainer.style.display = 'none';
//   }
// };

// document.addEventListener('DOMContentLoaded', () => {
//   const closeButtons = document.querySelectorAll('.close-btn');
//   closeButtons.forEach(button => {
//     button.addEventListener('click', (event) => {
//       const buttonData = event.target.dataset.messageCategory;
//       const xhr = new XMLHttpRequest();
//       xhr.open('POST', '/close_flash_message', true);
//       xhr.setRequestHeader('Content-Type', 'application/json');
//       xhr.onreadystatechange = function() {
//         if (xhr.readyState === 4) {
//           if (xhr.status === 200) {
//             // Message removed successfully, hide container
//             closeMessage(event.target.parentElement);
//           } else {
//             console.error('Error closing message:', xhr.status);
//           }
//         }
//       };
//       xhr.send(JSON.stringify({ category: buttonData }));
//     });
//   });
// });




function clearForm() {
  document.getElementById('feedback-form').reset();
}

