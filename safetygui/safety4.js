// Handle file selection for image and video uploads
document.getElementById('image-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        alert(`Image selected: ${file.name}`);
    }
});

document.getElementById('video-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        alert(`Video selected: ${file.name}`);
    }
});