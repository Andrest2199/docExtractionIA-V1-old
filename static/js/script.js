document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("uploadForm");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);
    let file = formData.get("file");

    getBase64(file, (base64_file) => {
      let requestBody = {
        filename: file.name,
        doctype: formData.get("tipo"),
        file_base64: base64_file,
      };

      fetch("http://127.0.0.1:8000/ocr_recognize", {
        method: "POST",
        body: JSON.stringify(requestBody),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          // Update divs with the information returned by the API
          let responseDiv = document.getElementById("response");
          responseDiv.innerText = "";
          for (let key in data) {
            let newElement = document.createElement("pre"); // Changed 'p' to 'pre'
            let value = data[key];
            // Check if value is an object and if so, convert it to a string
            if (typeof value === "object" && value !== null) {
              value = JSON.stringify(value, null, 2); // Convert to JSON string with indentation
            }
            newElement.textContent = `${key}: ${value}`;
            responseDiv.appendChild(newElement);
          }

          // Clear the form after receiving the response
          form.reset();
        })
        .catch((error) => {
          console.error("Error when submitting the form:", error);
        });
    });
  });
});

function getBase64(file, callback) {
  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    callback(reader.result);
  };
  reader.onerror = function (error) {
    console.log("Error: ", error);
  };
}
