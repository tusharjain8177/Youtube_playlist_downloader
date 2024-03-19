document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector("form");
    var progressBar = document.getElementById("progress-bar");
    var progressDiv = document.getElementById("progress");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        var playlistUrl = document.getElementById("playlist_url").value;
        if (playlistUrl) {
            progressDiv.style.display = "block";
            fetch("/download", {
                method: "POST",
                body: new URLSearchParams(new FormData(form))
            })
            .then(response => response.json())
            .then(data => {
                var interval = setInterval(function() {
                    progressBar.value = data.progress;
                    if (data.progress === 100) {
                        clearInterval(interval);
                        progressDiv.style.display = "none";
                    }
                }, 1000);
            })
            .catch(error => console.error("Error:", error));
        } else {
            alert("Please enter a valid playlist URL.");
        }
    });
});
