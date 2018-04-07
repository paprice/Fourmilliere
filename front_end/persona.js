
random = Math.floor((Math.random() * 5) + 1);

personas = ['duty_fullfiller', 'mechanic', 'nurturer', 'thinker', 'scientist'];

address = "http://localhost:5002"

ID = -1;

total_coins = 0;
last_weight = 0;

function load_random_persona(){
    persona = personas[random - 1];
    document.getElementById('persona').innerHTML = 'Yay you are an ' + persona + '!';

    var xhr = new XMLHttpRequest();
    xhr.open("POST", address + "/persons", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                ID = xhr.responseText;
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    // xhr.onerror = function (e) {
    // console.error(xhr.statusText);
    // };
    xhr.send('{"name": "Steve", "perso": "' + persona + '"}');

}


function get_tasks(){
    if (ID == -1){
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("GET", address + "/persons/"+ID+"/next", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                tasks = JSON.parse(xhr.responseText);
                last_weight = tasks['weight'];
                last_task = tasks['name']
                document.getElementById('tasks').innerHTML = '<p>You have to : ' + tasks['name'] + '</p>';
                document.getElementById('tasks').innerHTML += '<p>By doing doing this, you would gain ' + tasks['weight'] + ' challenge coins.'
                document.getElementById('tasks').innerHTML += '<button onclick="send_tasks()">Complete a task !</button>';
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    // xhr.onerror = function (e) {
    // console.error(xhr.statusText);
    // };
    xhr.send(null);

}

function send_tasks(){
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", address + "/persons/"+ID, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                //ID = xhr.responseText;
                total_coins += last_weight;
                alert('Congratulations ! Your current challenge coins balance is ' + total_coins);
                document.getElementById('tasks').innerHTML = '<button onclick="get_tasks()">Get Tasks !</button>';
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    // xhr.onerror = function (e) {
    // console.error(xhr.statusText);
    // };
    xhr.send('{"name": "' + last_task + '"}');

    
}