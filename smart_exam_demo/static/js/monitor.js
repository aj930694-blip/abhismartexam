const video = document.getElementById('video');
const warning = document.getElementById('warning');

if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
  warning.textContent = 'Camera access is not supported by your browser.';
} else {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    })
    .catch(() => {
      warning.textContent = 'Please allow camera access to start the exam.';
    });
}

window.addEventListener('blur', () => {
  warning.textContent = 'Please do not leave the exam page.';
});

window.addEventListener('focus', () => {
  warning.textContent = '';
});
