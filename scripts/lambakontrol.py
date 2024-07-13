#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32, Float64

class SignalController:
    def __init__(self):
     
        self.signal_pub = rospy.Publisher('/signal_status', Int32, queue_size=10)
    
        #self.steering_angle_pub = rospy.Publisher('/beemobs/FeedbackSteeringAngle', Float64, queue_size=10)
       
        rospy.Subscriber('/beemobs/FeedbackSteeringAngle', Float64, self.steering_angle_callback)
        rospy.Subscriber('/goal_status', Int32, self.goal_status_callback)
        
        
        self.at_goal = False

    def steering_angle_callback(self, msg):
        if not self.at_goal:   #hedefe varamadıysak
            if msg.data < -8:
                self.signal_pub.publish(1)  
            elif msg.data > 8:
                self.signal_pub.publish(2)  
            else:
                self.signal_pub.publish(0)  
        else:
            self.signal_pub.publish(3) 
            print('Hedefe Varıldı') 

    def goal_status_callback(self, msg):
        if msg.data == 1:
            self.at_goal = True 
        elif msg.data == 0:
            self.at_goal = False

            
if __name__ == '__main__':
    rospy.init_node('signal_controller')
    controller = SignalController()
    rospy.spin()



#RC_SignalStatus : Bu sinyal araç çalışıyorken sağ ,sol sinyal ve dörtlü flashörleri kontrol
#eden sinyaldir.
# 0 : Kapalı ( Sağ Sol Sinyal Kapalı )
# 1 : Sağ Sinyal
# 2 : Sol Sinyal
# 3 : Flashor (Dörtlü)