
random = Math.floor((Math.random() * 5) + 1);

personas = ['duty fulfiller', 'mechanic', 'nurturer', 'thinker', 'scientist'];

function load_random_persona(){
    persona = personas[random - 1];
    document.getElementById('persona').innerHTML = 'Yay you are an ' + persona + '!';

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://172.20.34.161:5002/persons", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log(xhr.responseText);
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    // xhr.onerror = function (e) {
    // console.error(xhr.statusText);
    // };
    xhr.send({"name": "a", "perso": "a"});

}