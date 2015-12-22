# 4chanGeneralTicker
A ticker for /general/ threads on 4chan.

A python service utilizes the basc-4chan library to find the /general/ thread
of your choice (but /rlg/ only right now), and prints the text replies in order
of posts. Saves the post id of the latest post in a text file, and references
on startup to resume from close to the same point it left off, if the thread
hasn't been updated.

To install the service, run "main.py install" in your python 3 interpreter.

You can then set the service to run during startup, or manually start it with
"NET START RLGTicker"

The service can be stopped with "NET STOP RLGTicker"


An arduino sketch accepts text strings 500 characters long and scrolls them
across a series of MAX7219 driver + LED matrix pairs.