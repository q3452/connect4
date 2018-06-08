# connect4
A command-line connect4 implementation in Python

This is a Python3 program with no non-standard dependencies (standard dependencies include: random, copy, time).  It should be OS independent, it was developer on Linux Mint 18.  It was developed in Python 3.5.2.

Unit testing can be performed using: python3 -m unittest -v test_app.py

Usage: python3 connect4.py

The main file connect4.py imports a number of player classes, by default, Human and ABpBot are used but there are also RandomBot and BasicBot.  These can be selected by instantiating them in lines 25-26 as players.

ABpBot is the main AI player of interest, it implements Alpha-Beta Pruning and can search to a depth of about 7 ply in reasonable time.