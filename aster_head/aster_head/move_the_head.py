import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from adafruit_servokit import ServoKit


class HeadSubscriber(Node):

    def __init__(self):
        super().__init__("move_the_head")
        self.sub_ = self.create_subscription(Int32, "move_head", self.msgCallback, 10)
        self.sub_
        self.kit = ServoKit(channels=16)
        #self.kit.servo[0].set_pulse_width_range(1000,2000)

    def msgCallback(self, msg):
        # self.get_logger().info("I heard: %s" % msg.data)
        self.kit.servo[1].angle = msg.data


def main():
    rclpy.init()

    head_subscriber = HeadSubscriber()
    rclpy.spin(head_subscriber)
    
    head_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
