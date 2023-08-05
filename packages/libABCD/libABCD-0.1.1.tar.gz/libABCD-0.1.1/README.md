# Autonomous Bariloche Central DAQ

## concept

The main concept for the DAQ is that it orbits around a central server. Control and information run through this server allowing a permanent follow-up of what is happening. The raw data is handled by the clients themselves and is not seen by the DAQ.
The server broadcasts its location by UDP to allow clients to connect. It keeps a list of clients and redirects messages as they are sent to the intendend client. All messages are JSON formatted. A ping-pong system ensure clients are up and running. Any connection not answering a ping within 30 seconds is closed.
The server itself is watchdogged so it is restarted if no proper action (touching a pid file) is done for 30 seconds.

## code

All the code is in the libABCD directory.
Exemple applications are in the examples directory. They include:
* abcdServer.py, the main server code
* S.py, a "spy" application that requests all messages being exchanged in the system and logs them
* exec-client.py, an example application that runs commands sent to it (warning, this is a huge security risk, do not run in unprotected environment)
* run.py, a run controller app that looks at an experiment description in a JSON file and runs the programs in screens and restarts them in case they die (includes the damicm.json example of JSON file)
* send.py, a simple message sender

running the exemples can be done by running in two windows abcdServer.py and run.py damicm, using send.py in a third to see what happens. Running S.py manually can also be interesting to see all messages going through.
