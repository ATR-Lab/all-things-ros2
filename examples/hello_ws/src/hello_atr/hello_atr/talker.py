"""Publish a greeting on the `chatter` topic at a fixed rate.

Parameters:
    greeting (string): text at the start of every message.
    publish_rate_hz (double): how many messages to publish per second.
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


def format_message(greeting: str, count: int) -> str:
    """Build the text of one message. Kept separate so it can be unit tested."""
    return f'{greeting} #{count}'


class Talker(Node):

    def __init__(self, **kwargs):
        # kwargs lets tests pass a private context or parameter overrides.
        super().__init__('talker', **kwargs)
        # Declare parameters with defaults; override them with --ros-args -p or a YAML file.
        self.declare_parameter('greeting', 'Hello from the ATR Lab')
        self.declare_parameter('publish_rate_hz', 2.0)

        rate = self.get_parameter('publish_rate_hz').value
        if rate <= 0.0:
            raise ValueError('publish_rate_hz must be greater than zero')

        self.count = 0
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0 / rate, self.publish_once)

    def publish_once(self):
        self.count += 1
        # Read the parameter on every tick so `ros2 param set` takes effect immediately.
        greeting = self.get_parameter('greeting').value
        msg = String()
        msg.data = format_message(greeting, self.count)
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
