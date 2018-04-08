address = "http://localhost:5002"

var myVar;

function StartTimer() {
    myVar = setInterval(GetMessages, 5000);
}


function GetMessages() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", address + "/gov", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var messages = JSON.parse(xhr.responseText);
                var count = messages['count']
                for (i = 0; i < count; i++) {
                    document.getElementById('record').innerHTML += messages['msg'][i]['message'] + "<br/>"
                }

                DeleteMessages()    
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(null);

}

function DeleteMessages() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", address + "/gov", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {

            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(null);
}

function ResetTasks(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", address + "/tasks", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {

            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(null);
}