# Description of our project

Our project is to make the WikipediaGame to find the midpoint of the start and end page.

We tried to find the start and end page as vector. After that if we find the mid point of those two vector.

That mid point vector can be the mid page of start and end page in Wikipedia, but if that mid point vector has no corresponding Wikipedia page, we find the nearest vector point that is corresponding with Wikipedia page.

If we successfully found the vector that corresponds with Wikipedia page, the output should be that Wikipedia page which is the mid page of start and end page.

# Algorithms we implemneted
We used word2vec to convert the start and end page into vector.

After that we calculate the mid vector which is the mid page between start and end.

# Installation instruction
Need to download our source code and have the right folder direction

install python 3.10

cd server

source setup.sh

python3.10 server.py

# Description of how we tested our project
We tested with start page as cat and end page as dog. The output of our program is wikipedia page of dog.

We also tested with start page as fish and end page as cat. The output of our program is wikipedia page of fish.

We have small dataset which contains so few words that the mid vector page does not show up. So sometimes, we get the start page and our mid vector which considered as the closest wikipedia page with the mid vector.

# Limitation and Future work
We made a project that uses Word2vec to get the position of the vector of the words in the database and find the midpoint between those two vectors. Our project is that the big database we planned was not downloaded to the computer, so we used a database with only basic words. Our database has fewer words, so the midpoint word usually is the Start Keyword or Finish Keyword that is close to the midpoint (this means there is no middle word between the two words in the database). That does not mean our project is not working.

As we mentioned above, our current database has few words that we cannot load wide range of words for our output. It is going to be solved if we download the whole database for Wikipedia.
For future work, our current output is just a midpoint between start and end. 
If we successfully implement the whole Wikipedia database in future, we can find all the mid page in Wikipedia and can go beyond our current situation.

We can use our midpoint algorithm to develope current route finding algorithm. We can use the midpoint that we first found as second endpoint and find another midpoint from original start page and our new endpage (midpage that we found). If we keep repeating this process, we will find the shortest path easily and quickly.
