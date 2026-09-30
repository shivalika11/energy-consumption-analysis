document.addEventListener("DOMContentLoaded", () => {

    const billFile = document.getElementById("billFile");
    const billFileName = document.getElementById("billFileName");

    const consumptionFile =
        document.getElementById("consumptionFile");

    const consumptionFileName =
        document.getElementById("consumptionFileName");

    const uploadButton =
        document.getElementById("uploadButton");


    // Show selected bill filename
    billFile.addEventListener("change", () => {

        if (billFile.files.length > 0) {
            billFileName.textContent =
                `Selected: ${billFile.files[0].name}`;
        } else {
            billFileName.textContent = "";
        }

    });


    // Show selected consumption filename
    consumptionFile.addEventListener("change", () => {

        if (consumptionFile.files.length > 0) {
            consumptionFileName.textContent =
                `Selected: ${consumptionFile.files[0].name}`;
        } else {
            consumptionFileName.textContent = "";
        }

    });


    // Temporary frontend upload action
    uploadButton.addEventListener("click", () => {

        const billSelected = billFile.files.length > 0;
        const consumptionSelected =
            consumptionFile.files.length > 0;

        if (!billSelected || !consumptionSelected) {
            alert("Please select both files before continuing.");
            return;
        }

        alert("Files selected successfully. Backend upload will be connected later.");

    });

});