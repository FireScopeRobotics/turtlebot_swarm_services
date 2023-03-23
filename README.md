sudo cp /home/ubuntu/turtlebot_swarm_services/services/ledstrip.service /lib/systemd/system/ledstrip.service
sudo cp /home/ubuntu/turtlebot_swarm_services/services/bmp390.service /lib/systemd/system/bmp390.service
sudo cp /home/ubuntu/turtlebot_swarm_services/services/mlx90640.service /lib/systemd/system/mlx90640.service

sudo chmod 744 /home/ubuntu/turtlebot_swarm_services/services/ledstrip.sh
sudo chmod 644 /lib/systemd/system/ledstrip.service

sudo chmod 744 /home/ubuntu/turtlebot_swarm_services/services/start_bmp390.sh
sudo chmod 644 /lib/systemd/system/bmp390.service

sudo chmod 744 /home/ubuntu/turtlebot_swarm_services/services/start_mlx.sh
sudo chmod 644 /lib/systemd/system/mlx90640.service

sudo systemctl start ...
sudo systemctl enable ...