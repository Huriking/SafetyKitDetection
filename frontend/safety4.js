async function uploadFile() {
  let fileInput = document.getElementById("uploadFile");
  let file = fileInput.files[0];

  if (!file) {
      alert("Please select a file first!");
      return;
  }

  let formData = new FormData();
  formData.append("file", file);

  let endpoint = file.type.startsWith("image") ? "/upload/image/" : "/upload/video/";

  let response = await fetch("http://127.0.0.1:8000" + endpoint, {
      method: "POST",
      body: formData
  });

  let data = await response.json();
  if (data.processed_image) {
      document.getElementById("outputImage").src = "http://127.0.0.1:8000/download/" + data.processed_image;
  }
  document.getElementById("reportLink").innerHTML = `<a href="http://127.0.0.1:8000/download/${data.report}" download>Download Report</a>`;
}
