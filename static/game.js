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
    if(str["message"] !== "No level found"){
        document.body.style.display = 'block';
        document.getElementById("titre").innerHTML = "Niveau " + str[3] + " : " + str[4]
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
                        if(grid[Math.floor(i / 8)][i % 8] !== 3 && grid[Math.floor(i / 8)][i % 8] !== 2){
                            if (cell.classList.contains('wall')) {
                                cell.classList.remove('wall');
                                grid[Math.floor(i / 8)][i % 8] = 0;
                            } else {
                                cell.classList.add('wall');
                                cell.classList.remove('floor');
                                grid[Math.floor(i / 8)][i % 8] = 1;
                            }
                        }
                    } else if (event.button === 2) { // Right-click
                        if(grid[Math.floor(i / 8)][i % 8] !== 3 && grid[Math.floor(i / 8)][i % 8] !== 2){
                            if (cell.classList.contains('floor')) {
                                cell.classList.remove('floor');
                            } else {
                                cell.classList.add('floor');
                                cell.classList.remove('wall');
                            }
                        }
                        grid[Math.floor(i / 8)][i % 8] = 0;
                    }
                    var id = cell.id.split(";")
                    UpdateNumbers(id[0], id[1])
                    CheckNumbers()
                });
            })(i);
            // Prevent context menu on right-click
            cell.addEventListener('contextmenu', function(event) {
                event.preventDefault();
            });

            for(var j =0; j<8;j++){
                document.getElementById("row-"+j).innerHTML = hintv[j]
                document.getElementById("col-"+j).innerHTML = hinth[j]
            }

            for(j =0; j<8;j++){
                UpdateNumbers(j,j)
            }
        }
    }else{
        window.location.href = "/lost";
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
        if(cptv !== parseInt(hintv[i]) || cpth !== parseInt(hinth[i])){
            document.getElementById("nextLevelBtn").style.display = "none";
            return
        }
    }
    document.getElementById("nextLevelBtn").style.display = "block";
}
function UpdateNumbers(row, col){
    var cptRow =0
    var cptCol =0
    for(var i =0; i<8;i++){
        if(grid[row][i] === 1){
            cptRow++;
        }
        if (grid[i][col] === 1){
            cptCol++;
        }
    }
    if(cptRow === parseInt(hintv[row])) {
        document.getElementById("row-"+row).style.color = "green";
    }else{
        document.getElementById("row-"+row).style.color = "red";
    }
    if(cptCol === parseInt(hinth[col])) {
        document.getElementById("col-"+col).style.color = "green";
    }else {
        document.getElementById("col-" + col).style.color = "red";
    }
}
