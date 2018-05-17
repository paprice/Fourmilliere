address = "http://server:5002"

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

function ResetTasks() {
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

function GetColonists() {
    document.getElementById('colonists').innerHTML = ""
    var xhr = new XMLHttpRequest();
    xhr.open("GET", address + "/persons", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var messages = JSON.parse(xhr.responseText);
                for (var i in messages) {
                    var key = i;
                    var val = messages[i];
                    for (var j in val) {
                        var sub_key = j;
                        var sub_val = val[j];
                        if (sub_key == "name") {
                            document.getElementById('colonists').innerHTML += sub_val 
                        }
                        if (sub_key == "coin") {
                            document.getElementById('colonists').innerHTML += '<font color="blue"> coin : '+ sub_val + '<font/><br/>'
                        }

                    }
                }
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(null);
}

function GetTasks() {
    document.getElementById('tasks').innerHTML = ""
    var xhr = new XMLHttpRequest();
    xhr.open("GET", address + "/tasks", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var messages = JSON.parse(xhr.responseText);
                for (var i in messages) {
                    var key = i;
                    var val = messages[i];
                    for (var j in val) {
                        var sub_key = j;
                        var sub_val = val[j];
                        if (sub_key == "name") {
                            document.getElementById('tasks').innerHTML += sub_val + "<br/>"
                        }
                    }
                }
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(null);
}