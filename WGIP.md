# Wikipedia Game Improvement Proposal

Authors: [Jooshin Kim,Andrew Kwon]

# Reflection on Thursday Lecture
After we talked with professor, we decided to work on the basic websocket before we actually work on our project.
We need to understand how to use websocket and how it works. We are planning to attend office hour and start the basic of websocket. That is our first milestone.

## Improvement

Right now the WikipediaGame doesn't end until the time limit. There is no "stop" button that user can interact with program during searching.
We proposed the modification that the user can interact with WikipediaGame especially the user can stop the searching in the middle of search phase.

Here's a high-level overview of how we could implement this:
 1 Set up a WebSocket server that can accept connections from clients. we can use a Python library like websockets or
   socket.io for this.
 2 Modify the client-side code to establish a WebSocket connection to the server when the page loads.
 3 Add a "stop" button to the client-side user interface. When this button is clicked, send a "stop" message over the
   WebSocket connection.
 4 Modify the server-side search code to check for "stop" messages at each step of the search. If it receives a "stop"
   message, stop the search.

#Pseudo-code for our modification.

In server/crawler.py:

 # Add a global variable to act as a stop signal
 stop_search = False

 def find_path(start_page, finish_page):
     # ...
     while queue and elapsed_time < TIMEOUT:
         # Check the stop signal at each step of the search
         if stop_search:
             break
         # ...


In server/server.py:

 from flask import Flask, request, jsonify, send_from_directory, Response
 from flask_limiter import Limiter
 from flask_limiter.util import get_remote_address
 import crawler

 app = Flask(__name__, static_folder='../client')
 limiter = Limiter(app=app, key_func=get_remote_address)

 @app.route('/stop_search', methods=['POST'])
 def stop_search():
     # Set the stop signal to True when a POST request is received
     crawler.stop_search = True
     return jsonify({'message': 'Search stopped.'}), 200

 # ...


On the client side:

 // When the user clicks the "stop" button...
 stopButton.addEventListener('click', function() {
     // Send a POST request to the /stop_search route
     fetch('/stop_search', {method: 'POST'});
 });