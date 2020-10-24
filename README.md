# arduino_web_serial_monitor
A serial monitor connected through a flask server running on the pc connected to the arduino board. This way you can test devices connected far away from the board.

![](/webpage.PNG)


**Use**
 1. Connect the board to a laptop/pc. **Make sure the device port is not being used!**
 2. Run the script. `python .\main.py -p your_port -b device_baud_rate`
    Example:  `python .\main.py -p COM14 -b 9600`
 3. Open the server on a web browser from any device connected on the same network. Server runs on port 80 so just type the server ip. 
