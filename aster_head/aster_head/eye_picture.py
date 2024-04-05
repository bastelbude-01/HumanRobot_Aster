from __future__ import unicode_literals
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
#Oled1306


from pathlib import Path
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image
from random import randrange
from time import sleep


class EyeSubscriber(Node):

    def __init__(self):
        super().__init__("show_eyes")
        self.sub_ = self.create_subscription(Int32, "eye_pic", self.msgCallback, 10)
        self.sub_
        self.oled_font = ImageFont.truetype('FreeSans.ttf', 20)
        self.auge ='\uf06e'
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial)
        self.serial2 = i2c(port=1, address=0x3D)
        self.device2 = ssd1306(self.serial2)
        

    def make_font(self, name, size):
        font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
        return ImageFont.truetype(font_path, size)

    def augen(self):
        self.font = self.make_font("fontawesome-webfont.ttf", self.device.height - 10)

        with canvas(self.device) as draw:
            left, top, right, bottom = draw.textbbox((0, 0), self.auge, self.font)
            w, h = right - left, bottom - top
            left = (self.device.width - w) / 2
            top = (self.device.height - h) / 2
            draw.text((left, top), text=self.auge, font=self.font, fill="white")
        with canvas(self.device2) as draw:
            left, top, right, bottom = draw.textbbox((0, 0), self.auge, self.font)
            w, h = right - left, bottom - top
            left = (self.device.width - w) / 2
            top = (self.device.height - h) / 2
            draw.text((left, top), text=self.auge, font=self.font, fill="white")

    def msgCallback(self, msg):
        self.get_logger().info("I heard: %s" % msg.data)
        if(msg.data == 1):
            self.augen()
        else:
            pass

        


def main():
    rclpy.init()

    eye_subscriber = EyeSubscriber()
    rclpy.spin(eye_subscriber)
    
    eye_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
