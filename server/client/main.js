document.getElementById('mid-point').addEventListener('click', function(event) {
    event.preventDefault();
    var startPage = document.getElementById('start-page').value.toLowerCase();
    var finishPage = document.getElementById('finish-page').value.toLowerCase();

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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            const wikipediaLink = document.getElementById('wikipedia-link');
            wikipediaLink.href = data.wikipedia_url;
            wikipediaLink.textContent = "Learn more on Wikipedia";
            wikipediaLink.style.display = "block"; // Show the link
            document.getElementById('midpoint-result').style.display = "block"; // Show the result section if hidden
            alert('Visit the provided link for more information.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request.');
    });
});
