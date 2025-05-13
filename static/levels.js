var scoreLevelSelect = document.getElementById('score-level-select');
scoreLevelSelect.addEventListener('change', function() {
    const selectedLevel = this.value;
    if (selectedLevel) {
        window.location.href = '/scores/' + selectedLevel;
    }
});

var globalScoresBtn = document.getElementById('global-scores-btn');
globalScoresBtn.addEventListener('click', function() {
    window.location.href = '/scores';
});
