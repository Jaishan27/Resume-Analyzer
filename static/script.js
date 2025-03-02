document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.getElementById("drop-area");
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  const output = document.getElementById("output");
  const loading = document.getElementById("loading");
  const jobTitleInput = document.getElementById("job-title");

  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.background = "#f0f0f0";
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.style.background = "";
  });

  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.style.background = "";
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      uploadFile(files[0]);
    }
  });

  uploadBtn.addEventListener("click", () => fileInput.click());

  document.getElementById("resetBtn").addEventListener("click", function () {
    window.location.href = "/"; // Redirects to the home page
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      uploadFile(fileInput.files[0]);
    }
  });

  function uploadFile(file) {
    if (!file.name.endsWith(".pdf") && !file.name.endsWith(".docx")) {
      alert("Only PDF and DOCX files are supported.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_title", jobTitleInput.value);

    dropArea.style.display = "none";
    loading.style.display = "inline-block";
    output.textContent = "";

    fetch("/upload", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        loading.style.display = "none";
        if (data.error) {
          output.textContent = "Error: " + data.error;
        } else {
          output.style.display = "block";
          output.textContent = `Match Percentage: ${
            data.match_percentage
          }%\n\nCommon Skills Found: ${
            data.resume_skills.join(", ") || "None"
          }\n\nMissing Skills: ${data.missing_skills.join(", ") || "None"}`;
        }
      })
      .catch(() => {
        loading.style.display = "none";
        output.textContent = "Error uploading file.";
      });
  }
});
