document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("uploadForm");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch("https://api.ono.starlight.science/ocr_recognize", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Actualizar los divs con la información devuelta por la API
            document.getElementById("serieFolio").innerText = data.SERIE_Y_FOLIO || "N/A";
            document.getElementById("tipoIncapacidad").innerText = data.TIPO_INCAPACIDAD || "N/A";
            // Agregar más campos aquí

            // Limpiar el formulario después de recibir la respuesta
            form.reset();
        })
        .catch(error => {
            console.error("Error al enviar el formulario:", error);
        });
    });
});
