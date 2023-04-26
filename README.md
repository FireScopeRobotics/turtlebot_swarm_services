# FireScope TurtleBot Services

This repo contains the necessary modules to bring up the add-ons to the TurtleBot

After cloning the repo initialise the submodules
```text
git submodule update --init
```
## MLX90640 Thermal Camera

The submodule is a fork of the MLX90640 driver made available by Pimoroni, the sensor interfaces through I2C

On the TurtleBot4's, a few additional dependencies are needed to build this module:

Make sure the Linux I2C dev library is installed and gstreamer plugins for the network streaming example:

```text
sudo apt-get install libi2c-dev
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-dev gstreamer1.0-tools gstreamer1.0-doc
sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good
```

To get the best out of the sensor modify `/boot/firmware/usercfg.txt`  (or `/boot/firmware/config.txt`) to change the I2C baudrate to 400 kHz:

```text
dtparam=i2c1=on,i2c1_baudrate=400000
```

Build the package in the `mlx90640` directory 
```text
cd mlx90640
make clean
make
```

The `rawrgb` example is used to stream the raw image buffer across the network using gstreamer.

```
sudo ./rawrgb | gst-launch-1.0 fdsrc blocksize=2304 ! udpsink host=enter-host-ip port=5000
```

On the recieving end (will also need the same gstreamer dependencies installed), run:
```
gst-launch-1.0 udpsrc blocksize=2304 port=5000 ! rawvideoparse use-sink-caps=false width=32 height=24 format=rgb framerate=16/1 ! videoconvert ! videoscale ! video/x-raw,width=640,height=480 ! autovideosink
```

The `mlx90640.service` brings up this pipeline to send the camera stream to multiple preset IPs found in `start_mlx.sh`

There's other cool examples available that wasn't used for this project, but you can learn more about it through the README in the module.


## BMP390 Barometric Pressure Sensor 

The submodule is a fork of the BMP390 driver made available by Adafruit, the sensor interfaces through SPI (or I2C)

It can be installed and used as a python pip package, but its much simpler directly use `BMP390/adafruit_bmp3xx.py`.

On the TurtleBot4's, a few additional dependencies are needed to build this module:

Install the adafruit-blinka package along with python3 GPIO packages for the Raspberry Pi

```text
sudo pip3 install adafruit-blinka
sudo apt-get install python3-dev python3-rpi.gpio
```

The `sensor_pub.py` script publishes pressure and temperature data from the sensor to `/sensor_topic` as a Float64MultiArray

The `bmp390.service` runs the script on startup, but sources .rosenv as root, this path may or may not change and is used in `start_bmp390.sh`


## LED Strips 

The module is a lot more straightforward, and only relies on the [Neopixel](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage) controller driver

```text
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka
```

The `led_controller.py` script listens to the wheel speeds on `/wheel_vels`, if the wheels spin the LEDs are turned on and alternate between red and blue.

The `ledstrip.service` runs the script on startup, but sources .rosenv as root, this path may or may not change and is used in `ledstrip.sh`



## Wiring Scheme

For reference, heres the wiring scheme with respect to the TurtleBot4 expansion PCBA [User I/O](https://turtlebot.github.io/turtlebot4-user-manual/electrical/pcba.html)

| Sensor     | Wiring (Sensor Board to User I/O)                                                                                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MLX90640   | VCC to Pin #2: 5V<br><br>GND to Pin #6: Ground<br><br>SDA to Pin #3: GPIO2, SDA I2C<br><br>SCL to Pin #5: GPIO3, SCL I2C                                                                               |
| BMP390     | VIN to Pin #1: 3.3V<br><br>GND to Pin #7: Ground<br><br>SCK to Pin #17: GPIO11, SCL SPI<br><br>SDA to Pin #13: GPIO10, MOSI SPI<br><br>SDO to Pin #15: GPIO9, MOSI SPI<br><br>CS to Pin #20: User port |
| LED Strips | VIN to Pin #4: 5V<br><br>GND to Pin #16: Ground<br><br>DATA to Pin #22: GPIO12, PWM                                                                                                                    |


## Services

Copy the service files to the relevant directories and change some permissions to run the shell scripts.
```text
sudo cp /home/ubuntu/turtlebot_swarm_services/services/ledstrip.service /lib/systemd/system/ledstrip.service
sudo cp /home/ubuntu/turtlebot_swarm_services/services/bmp390.service /lib/systemd/system/bmp390.service
sudo cp /home/ubuntu/turtlebot_swarm_services/services/mlx90640.service /lib/systemd/system/mlx90640.service

sudo chmod 744 /home/ubuntu/turtlebot_swarm_services/services/ledstrip.sh
sudo chmod 644 /lib/systemd/system/ledstrip.service

sudo chmod 744 /home/ubuntu/turtlebot_swarm_services/services/start_bmp390.sh
sudo chmod 644 /lib/systemd/system/bmp390.service

sudo chmod 744 /home/ubuntu/turtlebot_swarm_services/services/start_mlx.sh
sudo chmod 644 /lib/systemd/system/mlx90640.service
```

Finally, each service can be started and enabled, say for `mlx90640`

```text
sudo systemctl start mlx90640.service 
sudo systemctl enable mlx90640.service
```