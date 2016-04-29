# serimon

A (very) basic Python serial monitor inspired on the also basic Arduino IDE serial monitor.


##### You can pass port and baud rate as arguments.

'''
usage: serimon.py [-h] [--port PORT] [--rate RATE]

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  serial port name/path
  --rate RATE  baud rate
'''

##### Special Commands

For now there two special commands:
-CTRL+P - sends the text with a ASCII 26 chracter at the end
-CTRL+E - sends the text witha a ASCII 27 (ESC) character at the end 


##### Dependencies

-pyserial
-npyscreen





