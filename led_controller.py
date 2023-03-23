import board
import neopixel
import time
import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from irobot_create_msgs.msg import WheelVels

num_pixels = 32
pin = board.D12

pixels = neopixel.NeoPixel(pin, num_pixels, brightness=1,auto_write=False)


class VelSub(Node):

    def __init__(self):
        super().__init__('vel_sub')

        self.timer = self.create_timer(2, self.timer_callback)
        self.turn_on = False
        self.subscription = self.create_subscription(
            WheelVels,
            '/wheel_vels',
            self.listener_callback,
            qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning

    def timer_callback(self):
        if self.turn_on:
            pixels.fill((255, 0, 0))
            pixels.show()
            time.sleep(1)
            pixels.fill((0, 0, 255))
            pixels.show()
        else:
            pixels.fill((0, 0, 0))
            pixels.show()
    def listener_callback(self, msg):
        if msg.velocity_left != 0.0:
            self.turn_on = True
        else:
            self.turn_on = False


def main(args=None):
    rclpy.init(args=args)

    sub = VelSub()

    rclpy.spin(sub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()