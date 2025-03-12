var grid = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]
var hinth,hintv

function loadGame(){
    var url="/init";
    var xhr= new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            initializeGrid(JSON.parse(xhr.response))
        }
    }
    xhr.open("POST",url,true);
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send();
}

function initializeGrid(str) {
    var i
    hinth = str[1]
    hintv = str[2]
    for ( i=0; i < str[0].length; i++) {
        const cell = document.getElementById(`${Math.floor(i / 8)};${i % 8}`);
        if (str[0][i] === "3") {
            cell.classList.add('chest');
            grid[Math.floor(i / 8)][i % 8] = 3;
        }
        if (str[0][i] === "2") {
            cell.classList.add('monster');
            grid[Math.floor(i / 8)][i % 8] = 2;
        }
        (function(i) {
            cell.addEventListener('mousedown', function(event) {
                if (event.button === 0) { // Left-click
                    if (cell.classList.contains('wall')) {
                        cell.classList.remove('wall');
                        grid[Math.floor(i / 8)][i % 8] = 0;
                    } else {
                        cell.classList.add('wall');
                        cell.classList.remove('floor');
                        grid[Math.floor(i / 8)][i % 8] = 1;
                    }
                } else if (event.button === 2) { // Right-click
                    cell.classList.add('floor');
                    cell.classList.remove('wall');
                    grid[Math.floor(i / 8)][i % 8] = 0;
                }
                CheckNumbers()
            });
        })(i);
        // Prevent context menu on right-click
        cell.addEventListener('contextmenu', function(event) {
            event.preventDefault();
        });
    }
}

function CheckNumbers() {
    for (let i = 0; i < grid.length; i++) {
        let cpth=0
        let cptv=0
        for (let j = 0; j < grid[i].length; j++) {
            if(grid[i][j] === 1){
                cptv++;
            }
            if(grid[j][i] === 1){
                cpth++;
            }

        }
        if(cptv !== parseInt(hintv[i])){
            console.log("ligne " + i + " : " +cptv, hintv[i])
            return
        }else if(cpth !== parseInt(hinth[i])){
            console.log("colonne " + i + " : "+ cpth, hinth[i])
            return
        }
    }

    console.log("ok")

}

loadGame()