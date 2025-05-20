document.addEventListener("DOMContentLoaded", function() {
    // Gestion des boutons de scores par niveau
    const scoreButtons = document.querySelectorAll(".score-btn");
    scoreButtons.forEach(button => {
        button.addEventListener("click", function() {
            const levelId = this.getAttribute("data-level-id");
            window.location.href = `/scores/${levelId}`;
        });
    });

    // Gestion du bouton des scores globaux
    const globalScoresBtn = document.getElementById("global-scores-btn");
    if (globalScoresBtn) {
        globalScoresBtn.addEventListener("click", function() {
            window.location.href = "/scores";
        });
    }
});