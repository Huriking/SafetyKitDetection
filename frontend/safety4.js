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
        }  else {
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

        // Reset displays
        imgElement.style.display = "none";

        // Handle Image Output
        if (data.processed_image) {
            imgElement.src = data.processed_image;
            imgElement.style.display = "block"; // Show image
        }
        
        // Handle JSON Report Download
        if (data.report) {
            // Assuming 'data.report' contains the path like './frontend/reports/image2_equipment_status_and_bar_chart_with_table.pdf'
            let reportUrl = data.report; // Example: './frontend/reports/image2_equipment_status_and_bar_chart_with_table.pdf'
            console.log("Report location:", reportUrl);
            
            // Normalize the path to forward slashes for consistency
            let normalizedPath = reportUrl.replace(/\\/g, '/');
            console.log("Normalized path name:", normalizedPath);
            
            // Extract the file name by splitting the string at the last '/'
            let fileName = normalizedPath.split('/').pop();
            console.log("Extracted file name:", fileName);
            
            // Construct the correct URL path for accessing the report in FastAPI (served from /reports endpoint)
            // Since FastAPI serves reports at /reports/{filename}, we can directly use the file name
            let downloadUrl = `/reports/${fileName}`;
            console.log("Download URL:", downloadUrl);
            
            // Set the link to the report
            const reportLink = document.getElementById('reportLink');
            reportLink.innerHTML = `<a href="${downloadUrl}" target="_blank" download="${fileName}">Download Report</a>`;
        } else {
            const reportLink = document.getElementById('reportLink');
            reportLink.innerHTML = ""; // Clear the link if no report is available
        }

    } catch (e) {
        console.log("Error in frontend:", e);
    }
}
async function uploadFile2() {
    try {
        let fileInput = document.getElementById("uploadFile2");

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
        if (file.type.startsWith("video")) {
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
        let videoElement = document.getElementById("outputVideo");


        videoElement.style.display = "none";


        // Handle Video Output
        if (data.processed_video) {
            videoElement.src = data.processed_video; // Set the video source
            videoElement.style.display = "block"; // Make the video element visible
    
            // Optionally auto-play the video
            videoElement.play();
        }
        // Handle JSON Report Download
        if (data.report) {
            // Assuming 'data.report' contains the path like './frontend/reports/image2_equipment_status_and_bar_chart_with_table.pdf'
            let reportUrl = data.report; 
            console.log("Report location:", reportUrl);
            
            // Normalize the path to forward slashes for consistency
            let normalizedPath = reportUrl.replace(/\\/g, '/');
            console.log("Normalized path name:", normalizedPath);
            
            // Extract the file name by splitting the string at the last '/'
            let fileName = normalizedPath.split('/').pop();
            console.log("Extracted file name:", fileName);
            
            // Construct the correct URL path for accessing the report in FastAPI (served from /reports endpoint)
            // Since FastAPI serves reports at /reports/{filename}, we can directly use the file name
            let downloadUrl = `/reports/${fileName}`;
            console.log("Download URL:", downloadUrl);
            
            // Set the link to the report
            const reportLink = document.getElementById('reportLink');
            reportLink.innerHTML = `<a href="${downloadUrl}" target="_blank" download="${fileName}">Download Report</a>`;
        } else {
            const reportLink = document.getElementById('reportLink');
            reportLink.innerHTML = ""; // Clear the link if no report is available
        }

    } catch (e) {
        console.log("Error in frontend:", e);
    }
}
window.addEventListener('beforeunload', function (event) {
    // Send a request to the endpoint
    fetch('/terminate', {
        method: 'POST',
        body: JSON.stringify({ message: 'User closed the page' }),
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => {
        // Handle response (optional)
    }).catch(error => {
        console.error('Error sending close event:', error);
    });
});
