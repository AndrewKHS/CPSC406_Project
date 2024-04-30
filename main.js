document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('wiki-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var startPage = document.getElementById('start-page').value;
        var finishPage = document.getElementById('finish-page').value;
        fetch('/find_path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start: startPage,
                finish: finishPage
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.path) {
                let pathHtml = '<ul>';
                data.path.forEach(page => {
                    pathHtml += `<li><a href="${page}">${decodeURIComponent(page)}</a></li>`;
                });
                pathHtml += '</ul>';
                document.getElementById('path').innerHTML = pathHtml;
            }
            if (data.logs) {
                let logsHtml = data.logs.join('<br>');
                document.getElementById('logs').innerHTML = logsHtml;
            }
            if (data.error) {
                document.getElementById('path').innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('mid-point').addEventListener('click', function() {
        var startPage = document.getElementById('start-page').value;
        var finishPage = document.getElementById('finish-page').value;
        fetch('/midpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start: startPage,
                finish: finishPage
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.midpoint_url) {
                alert('Midpoint URL: ' + data.midpoint_url);
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});