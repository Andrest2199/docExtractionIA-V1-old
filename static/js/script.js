document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("uploadForm");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);
    let file = formData.get("file");

    getBase64(file, (base64_file) => {
      //   console.log("base64_file", base64_file);

      let requestBody = {
        filename: file.name,
        doctype: formData.get("tipo"),
        file_base64: base64_file,
      };
      //   console.log(requestBody);
      fetch("http://127.0.0.1:8000/ocr_recognize", {
        method: "POST",
        body: JSON.stringify(requestBody),
        headers: {
          "Content-Type": "application/json",
          //   "x-api-key":
          //     "c2tfdGVzdF9hcGlfa2V5XzIwMjEgrupo-ono-92f3fdbd-633c-4487-bead-4c311a60a1c7",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          // Actualizar los divs con la información devuelta por la API
          document.getElementById("response").innerText =
            JSON.stringify(data) || "N/A";
          // Agregar más campos aquí

          // Limpiar el formulario después de recibir la respuesta
          form.reset();
        })
        .catch((error) => {
          console.error("Error al enviar el formulario:", error);
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
