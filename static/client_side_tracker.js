window.onload = function () {
    test = localStorage.getItem("u");
    if (test === null) {
        var possible = "0123456789";
        var text = "";
        for (var i = 0; i < parseInt(document.getElementById("tracker").getAttribute("data-cookie-length")); i++)
            // https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        localStorage.setItem("u", text);
    }
    var url_start = document.getElementById("tracker").getAttribute("data-next-site")
    var combined_id = document.getElementById("tracker").getAttribute("data-combined-id")
    var safe_referer = document.getElementById("tracker").getAttribute("data-safe_referer")
    // If combined id exists it is added (in which case we are chaining the cookies), otherwise appends empty string 
    var next_site = url_start + '/' + (combined_id || "") + localStorage.getItem("u") + '/safe-referer?id=' + safe_referer;
    setTimeout(function () {
        window.location = next_site;
    }, combined_id ? 100 : 1000);
};


