A description of your project, including of the algorithms you implemented.

installation instructions that enable me to run and test your project.

A description of how you tested your project and how I can reproduce your test results.

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

source setup.sh

python server.py

# Description of how we tested our project
We tested with start page as cat and end page as dog. The output of our program is wikipedia page of dog.

We also tested with start page as fish and end page as cat. The output of our program is wikipedia page of fish.

We have small dataset which contains so few words that the mid vector page does not show up. So sometimes, we get the start page and our mid vector which considered as the closest wikipedia page with the mid vector.
