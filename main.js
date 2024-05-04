document.getElementById('mid-point').addEventListener('click', function(event) {
    event.preventDefault();
    var startPage = document.getElementById('start-page').value;
    var finishPage = document.getElementById('finish-page').value;

    fetch('/midpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start: startPage,
            end: finishPage
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            document.getElementById('start-summary').textContent = `Start summary: ${data.start_page}`;
            document.getElementById('end-summary').textContent = `End summary: ${data.end_page}`;
            const wikipediaLink = document.getElementById('wikipedia-link');
            wikipediaLink.href = data.wikipedia_url;
            wikipediaLink.textContent = "Learn more on Wikipedia";
            wikipediaLink.style.display = "block"; // Show the link
            document.getElementById('midpoint-result').style.display = "block"; // Show the results
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request.');
    });
});
