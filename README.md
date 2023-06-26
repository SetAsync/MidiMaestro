# MidiMaestro
Created for Piotr Barcz.

This is a Discord bot designed to allow you and other members to control a single MIDI output (for streams and other purposes).
https://www.youtube.com/@PiotrBarcz

I am not profficent in python, this code is not pythonic and hardly efficent.
This project is a combination of my hate for python, and LUA's lack of a good MIDI module.

Commands:
.help - Shows the information message.
.add (attachment) - Will add the attachment to the queue.
.queue - Shows the queue, and your position in it.
.setup [a] [b] - Provide no arguments to see your options.

Information:
Queued files will be added to "files" and their file name will become the authors User ID.
These files are deleted when played, and the directory is cleared when the bot starts (in case of errors).

Every one second the bot checks the queue, if something is present it will be removed and player, the loop will wait for the track to complete before its next check.
If no tracks are waiting, the bot will play a random file (as long as autoplay is on).

I am not completely confident in how secure validating file downloads by their extension is, use this system at your own risk.
