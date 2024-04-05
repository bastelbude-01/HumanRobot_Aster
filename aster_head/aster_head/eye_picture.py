import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class EyeSubscriber(Node):

    def __init__(self):
        super().__init__("show_eyes")
        self.sub_ = self.create_subscription(Int32, "eye_pic", self.msgCallback, 10)
        self.sub_

    def msgCallback(self, msg):
        self.get_logger().info("I heard: %s" % msg.data)


def main():
    rclpy.init()

    eye_subscriber = EyeSubscriber()
    rclpy.spin(eye_subscriber)
    
    eye_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
