document.addEventListener('DOMContentLoaded', function () {
    function controlDevice(device, state) {
        console.log("controlDevice called with device:", device, "state:", state);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/control", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                console.log("Response from server:", xhr.responseText);
            }
        };
        var data = JSON.stringify({device: device, state: state});
        console.log("Sending data:", data);
        xhr.send(data);
    }

    function fetchValue() {
        console.log("Fetching value");
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/get_value", true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                console.log("Value fetched: ", response.value);
                var valueElement = document.getElementById('valueDisplay');
                if (valueElement) {
                    valueElement.innerText = response.value;
                } else {
                    console.error('Element with ID "valueDisplay" not found.');
                }
            } else if (xhr.readyState == 4) {
                console.error('Failed to fetch value:', xhr.statusText);
            }
        };
        xhr.send();
    }

    function fetchInputState() {
        console.log("Fetching input state");
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/read_input", true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                console.log("Input state fetched: ", response.input_state);
                var inputStateText = response.input_state === 1 ? 'HIGH' : 'LOW';
                var inputStateElement = document.getElementById('inputStateDisplay');
                if (inputStateElement) {
                    inputStateElement.innerText = inputStateText;
                } else {
                    console.error('Element with ID "inputStateDisplay" not found.');
                }
            } else if (xhr.readyState == 4) {
                console.error('Failed to fetch input state:', xhr.statusText);
            }
        };
        xhr.send();
    }

    setInterval(fetchValue, 1000); // Met à jour la valeur toutes les secondes
    setInterval(fetchInputState, 1000); // Met à jour l'état de la broche d'entrée toutes les secondes

    window.controlDevice = controlDevice;
});
