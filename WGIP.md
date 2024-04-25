# Wikipedia Game Improvement Proposal

Authors: [Jooshin Kim,Andrew Kwon]

# New Project 
We decided to change our project. 
Our new idea is to find midpoint of start and end page. 
We are using world2vec to have the vectors correspond to start and end. In the vector, we can calculate the midpoint vector which will be correspond with midpoint of two pages (start, end).
If the midpoint vector does not correspond with any page in Wikipedia, we want to find nearest vector which is the actual Wikipedia page.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Milestones
4/3: Understand the concept of websocket and research on how to use it. Write report about it.

4/10: Get feedback on our report and discuss with Dr. Kurz about it as he told us to do. Practice it with simple program before implementing on WikipediaGame.

5/8: Implement it into WikipediaGame and debugging.

# Feedback from Dr. Kurz 4/9
Don't make just normal stop button.
Use websocket, find midpoint between start and end.

# Short report on websocket for WikipediaGame 4/3/2024
WebSockets are a protocol that allows for real-time, two-way communication between a client and a server over a single, long-lived connection.
In other words, WebSockets allow for an interactive communication session between the user's browser and the server, enabling you to send messages to the server (like a stop command) and handle them in real-time.

Server
1. We need to set up a Websocket server.
2. Define a route that upgrades HTTP requests to WebSocket requests.
3. On a new WebSocket connection, assign a unique session ID to each game or user.
4. Listen for messages from the client, such as a "stop" command.
5. Pathfinding logic should periodically check for a "stop" flag that can be set when a WebSocket message is received. Upon receiving a stop message, halt the pathfinding process and optionally return the current path or state.

Client
1. When the game starts, open a WebSocket connection to the server using the WebSocket API. Ensure that the connection remains open during the game session.
2. Implement a UI element (e.g., a stop button). When clicked, send a message over the WebSocket connection to the server indicating that the pathfinding should be stopped.
Handle any acknowledgments or messages from the server, such as confirmation of stopping the process.
3. Listen for messages from the server to receive commands or updates, such as halting the pathfinding process.

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