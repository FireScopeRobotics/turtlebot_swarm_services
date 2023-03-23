#!/usr/bin/env bash
bash -c "./home/ubuntu/turtlebot_swarm_services/mlx90640/examples/rawrgb | gst-launch-1.0 fdsrc blocksize=2304 ! multiudpsink clients=192.168.23.7:5000,192.168.23.7:5001"
