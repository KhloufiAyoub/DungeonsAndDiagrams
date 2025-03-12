function loadGame(){
    var url="/init";
    var xhr= new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            initializeGrid(JSON.parse(xhr.response))
            console.log(xhr.response)
            console.log(JSON.parse(xhr.response))
        }
    }
    xhr.open("POST",url,true);
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send();
}

function initializeGrid(str) {
    for (var i = 0; i < str[0].length; i++) {
        const cell = document.getElementById(`${Math.floor(i / 8)}-${i % 8}`);
        if (str[0][i] === "3") {
            cell.classList.add('chest');
        }
        if (str[0][i] === "2") {
            cell.classList.add('monster');
        }
        // Add click event listener to toggle 'wall' class on left-click
        cell.addEventListener('click', function(event) {
            if (event.button === 0) { // Left-click
                cell.classList.toggle('wall');
            }
        });
        // Prevent context menu on right-click
        cell.addEventListener('contextmenu', function(event) {
            event.preventDefault();
        });
    }
}

loadGame()