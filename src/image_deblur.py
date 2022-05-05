#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import numpy as np

class Deblur_node(object):
    def __init__(self):
        # Params
        self.image = None
        self.new_image = None
        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.ros_rate = float(rospy.get_param('~ros_rate', '30.0'))
        self.loop_rate = rospy.Rate(self.ros_rate)

        self.deblur_thresh = float(rospy.get_param('~deblur_thresh', '500.0'))

        self.image_in_topic = rospy.get_param('~image_in_topic')
        self.image_out_topic = rospy.get_param('~image_out_topic')

        self.crop_bottom = rospy.get_param('~crop_bottom')
        self.debug = rospy.get_param('~debug')
        self.deblur = rospy.get_param('~deblur')
        # Subscribers
        rospy.Subscriber(self.image_in_topic,Image,self.callback, queue_size=20)

        # Publishers
        self.pub = rospy.Publisher(self.image_out_topic, Image,queue_size=20)

    def variance_of_laplacian(self):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(self.image.copy(), cv2.CV_64F).var()


    def callback(self, msg):
        # rospy.loginfo('Image received...')
        self.image = self.br.imgmsg_to_cv2(msg,desired_encoding='rgb8')

        value = self.variance_of_laplacian()
        if(self.debug):
            print(value)
        if(self.deblur):
            if (value < self.deblur_thresh):
                # rospy.loginfo("Blueeeeeeeeeeeerrrrrrrrrrrrrrr")
                kernel = np.array([[-1, -1, -1],
                       [-1, 9,-1],
                       [-1, -1, -1]])
                start_point = (0,240)
                end_point = (480,320)
                color = (0,0,0)
                thickness = -1

                if(self.crop_bottom):
                    self.image = cv2.rectangle(self.image, start_point, end_point, color, thickness)
                self.image = cv2.GaussianBlur(self.image,(3,3),4)

                self.new_image = cv2.filter2D(src=self.image, ddepth=-1, kernel=kernel)
            else:
                start_point = (0,240)
                end_point = (480,320)
                color = (0,0,0)
                thickness = -1
                if(self.crop_bottom):
                    self.new_image = cv2.rectangle(self.image, start_point, end_point, color, thickness)
        else:
            start_point = (0,240)
            end_point = (480,320)
            color = (0,0,0)
            thickness = -1
            self.new_image = cv2.rectangle(self.image, start_point, end_point, color, thickness)


    def start(self):
        rospy.loginfo("Deblur Node Up!")
        #rospy.spin()
        while not rospy.is_shutdown():
            
            #br = CvBridge()
            if self.new_image is not None:
                self.pub.publish(self.br.cv2_to_imgmsg(self.new_image.copy(), encoding='rgb8'))
                self.new_image = None
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node("imagedeblur", anonymous=True)
    my_node = Deblur_node()
    my_node.start()