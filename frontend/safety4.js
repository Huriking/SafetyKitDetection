async function uploadFile() {
    try {
        let fileInput = document.getElementById("uploadFile");

        // Ensure the file input exists
        if (!fileInput) {
            alert("File input not found!");
            return;
        }

        let file = fileInput.files[0];

        // Debugging: Check if file is being detected
        console.log("Selected File:", file);

        if (!file) {
            alert("Please select a file first!");
            return;
        }

        let formData = new FormData();
        formData.append("file", file);

        let endpoint;
        if (file.type.startsWith("image")) {
            endpoint = "/upload/image/";
        } else if (file.type.startsWith("video")) {
            endpoint = "/upload/video/";
        } else {
            alert("Unsupported file type. Please upload an image or a video.");
            return;
        }

        console.log("Uploading to:", endpoint);

        let response = await fetch("http://127.0.0.1:8000" + endpoint, {
            method: "POST",
            body: formData,
        });

        let data = await response.json();
        console.log("Response Data:", data);

        // Elements
        let imgElement = document.getElementById("outputImage");
        let videoElement = document.getElementById("outputVideo");

        // Reset displays
        imgElement.style.display = "none";
        videoElement.style.display = "none";

        // Handle Image Output
        if (data.processed_image) {
            imgElement.src = "data:image/jpeg;base64," + data.processed_image;
            imgElement.style.display = "block"; // Show image
        }

        // Handle Video Output
        if (data.processed_video) {
            let videoBlob = base64ToBlob(data.processed_video, "video/mp4");
            let videoUrl = URL.createObjectURL(videoBlob);
            videoElement.src = videoUrl;
            videoElement.controls = true;
            videoElement.style.display = "block"; // Show video
        }

        // Handle JSON Report Download
        let reportLink = document.getElementById("reportLink");
        if (data.report) {
            let reportBlob = new Blob([JSON.stringify(data.report, null, 4)], { type: "application/json" });
            let reportUrl = URL.createObjectURL(reportBlob);
            reportLink.innerHTML = `<a href="${reportUrl}" download="report.json">Download Report</a>`;
        } else {
            reportLink.innerHTML = "";
        }

    } catch (e) {
        console.log("Error in frontend:", e);
    }
}

// Convert Base64 to Blob for Video Playback
function base64ToBlob(base64, mimeType) {
    let byteCharacters = atob(base64);
    let byteArrays = [];
    for (let i = 0; i < byteCharacters.length; i++) {
        byteArrays.push(byteCharacters.charCodeAt(i));
    }
    let byteArray = new Uint8Array(byteArrays);
    return new Blob([byteArray], { type: mimeType });
}
