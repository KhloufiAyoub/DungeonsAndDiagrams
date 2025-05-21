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

// Fonction pour charger l'image d'un niveau via une requête AJAX
function loadLevelImage(levelId) {
    var imgDiv = document.getElementById(`lvl-img-${levelId}`);
    if (imgDiv) {
        // Créer un élément img
        var img = document.createElement("img");
        img.src = `/level-image/${levelId}`; // URL directe vers l'image
        img.alt = `Image du niveau ${levelId}`;
        img.onerror = function() {
            console.error(`Erreur lors du chargement de l'image pour le niveau ${levelId}`);
        };
        imgDiv.appendChild(img);
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