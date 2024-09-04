#!/usr/bin/python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class Converter(Node):
    def __init__(self):
        super().__init__('msg_to_mp4')
        self.image_subscription = self.create_subscription(
            Image,
            '/zed/zed_node/rgb/image_rect_color',
            self.callback,
            10)
        self.image_subscription
        
        self.out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 15, (1104, 621))
        # self.out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 1.0, (640, 360))
        
    def callback(self, data: Image):
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
        print(cv_image.shape)
        self.out.write(cv_image)
    
    def save(self):
        self.out.release()  
         
def main(args=None):
    try:
        rclpy.init(args=args)
        converter = Converter()
        rclpy.spin(converter)
    except KeyboardInterrupt:
        converter.save()
        print("Video has been saved.")
    finally:
        converter.destroy_node()
        rclpy.shutdown()
        

if __name__ == '__main__':
    main()