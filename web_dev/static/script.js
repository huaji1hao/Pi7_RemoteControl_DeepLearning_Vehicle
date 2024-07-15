function limitInput(event) {
    if (event.target.value.length > 2) {
        event.target.value = event.target.value.slice(0, 2);
    }
}

function sendCommand(event) {
    event.preventDefault(); // 阻止表单默认提交行为

    const command = document.getElementById("command_input").value;
    document.getElementById("command_input").value = "";  // 立即清除输入框内容

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_command", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const jsonResponse = JSON.parse(xhr.responseText);
            document.getElementById("current_command").innerText = jsonResponse.last_command;
            if (jsonResponse.last_command === 'r') {
                displayRecords(jsonResponse.records);  // 传递 jsonResponse.records
            } else {
                document.getElementById("response").innerText = "Arduino Response: " + jsonResponse.response;
            }
        }
    };
    xhr.send("command=" + command);
}

function displayRecords(records) {
    const recordsContainer = document.getElementById("records_container");
    recordsContainer.innerHTML = "";

    records.forEach(record => {
        const recordElement = document.createElement("div");
        recordElement.innerText = `ID: ${record.id}, Filename: ${record.filename}, Result: ${record.result}`;
        recordsContainer.appendChild(recordElement);
    });
}
