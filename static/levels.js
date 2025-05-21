document.addEventListener("DOMContentLoaded", function() {
    // Gestion des boutons de scores par niveau
    var scoreButtons = document.querySelectorAll(".score-btn");
    scoreButtons.forEach(button => {
        button.addEventListener("click", function() {
            const levelId = this.getAttribute("data-level-id");
            window.location.href = `/scores/${levelId}`;
        });
    });

    // Gestion du bouton des scores globaux
    var globalScoresBtn = document.getElementById("global-scores-btn");
    if (globalScoresBtn) {
        globalScoresBtn.addEventListener("click", function() {
            window.location.href = "/scores";
        });
    }
});

// fonction pour aller chercher avec un requete AJAX l'image du niveau et l'afficher dans la div avec comme id lvl-img-{{l'id du niveau}}
function loadLevelImage(levelId) {
    var imgDiv = document.getElementById(`lvl-img-${levelId}`);
    if (imgDiv) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", `/level-image/${levelId}`, true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var img = document.createElement("img");
                img.src = response.image; // L'image est déjà en base64 (data:image/png;base64,...)
                img.alt = `Image du niveau ${levelId}`;
                imgDiv.appendChild(img);

            } else {
                console.error("Erreur lors du chargement de l'image du niveau.");
            }
        };
        xhr.send();
    }
}
// Fonction pour charger les images de tous les niveaux
function loadAllLevelImages() {
    var levelIds = Array.from(document.querySelectorAll("[id^='lvl-img-']")).map(div => div.id.split('-')[2]);
    levelIds.forEach(levelId => {
        loadLevelImage(levelId);
    });
}
loadAllLevelImages();