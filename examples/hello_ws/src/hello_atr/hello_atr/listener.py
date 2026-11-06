"""Subscribe to the `chatter` topic and log every message."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):

    def __init__(self, **kwargs):
        super().__init__('listener', **kwargs)
        self.received = 0
        self.subscription = self.create_subscription(String, 'chatter', self.on_message, 10)

    def on_message(self, msg: String):
        self.received += 1
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
