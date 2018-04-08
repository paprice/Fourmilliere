random = Math.floor((Math.random() * 5) + 1);

personas = ['duty_fullfiller', 'mechanic', 'nurturer', 'thinker', 'scientist'];

address = "http://localhost:5002"

ID = -1;

total_coins = 0;
last_weight = 0;

function load_random_persona() {
    persona = personas[random - 1];
    document.getElementById('persona').innerHTML = 'Your AI have determined that you are a <font color="red">' + persona + '</font>!';
    var xhr = new XMLHttpRequest();
    xhr.open("POST", address + "/persons", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                ID = xhr.responseText;
                document.getElementById('askName').style.display = "none"
                document.getElementById('nameRegister').style.display = "block"
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    // xhr.onerror = function (e) {
    // console.error(xhr.statusText);
    // };
    var name = document.getElementById('nameInput').value
    xhr.send('{"name": "' + name + '" , "perso": "' + persona + '"}');

}


function get_tasks() {
    if (ID == -1) {
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("GET", address + "/persons/" + ID + "/next", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                tasks = JSON.parse(xhr.responseText);
                last_weight = tasks['weight'];
                last_task = tasks['name']
                document.getElementById('tasks').innerHTML = '<p>You have to : <font color="red">' + tasks['name'] + '</font></p>';
                document.getElementById('tasks').innerHTML += '<p>By doing doing this, you would gain ' + tasks['weight'] + ' challenge coins.';
                document.getElementById('completeTask').style.display = "block";
                document.getElementById('getTask').style.display = "none";

                //document.getElementById('tasks').innerHTML += '';
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

function send_tasks() {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", address + "/persons/" + ID, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                ret = JSON.parse(xhr.responseText);
                coin = ret['coin']
                //alert(coin)
                //ID = xhr.responseText;
                //total_coins += last_weight;
                // alert('Congratulations ! Your current challenge coins balance is ' + coin);
                document.getElementById('challengeCoin').innerHTML = "You have currently " + coin + " challenge coin in your possession"
                document.getElementById('completeTask').style.display = "none";
                document.getElementById('getTask').style.display = "block";
                document.getElementById('tasks').innerHTML = ''

                document.getElementById('taskDone').innerHTML += last_task + "<br/>"
                // document.getElementById('tasks').innerHTML = '<button onclick="get_tasks()">Get Tasks !</button>';
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