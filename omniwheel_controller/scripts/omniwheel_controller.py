#!/usr/bin/env python3
import socket
import numpy as np 
import math
import matplotlib.pyplot as plt


import rospy
import tf
import tf2_ros
import threading
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped

# Distance du centre du robot aux roues (m)
L = 0.13  # 13 cm
sqrt3 = np.sqrt(3)


class OmniOdometry:
    def __init__(self):
        rospy.init_node('omni_odometry_node')

        # Initialisation
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = rospy.Time.now()

        # Subscriber des vitesses des roues
        rospy.Subscriber('/wheel_velocities', Float32MultiArray, self.velocity_callback)

        # Publisher Odometry
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)

        # Broadcaster TF
        self.odom_broadcaster = tf2_ros.TransformBroadcaster()

        thread = threading.Thread(target=self.velocity_callback)
        thread.start() 

        rospy.loginfo("Nœud d'odométrie omnidirectionnelle démarré.")
        rospy.spin()

    def Kinematic_direct(self,V1,V2,V3): 
        Vx = -0.5 * V3 - 0.5 * V2 + V1
        Vy = sqrt3 * V3 - sqrt3 * V2 
        Wz = (1/L) * V3 + (1/L) * V2 + (1/L) * V1
        return (Vx,Vy,Wz)

    def Kinematic_reverse(self,Vx,Vy,Wz): 
        V1 = Vx + (Wz * L)
        V2 = -0.5 * Vx - (sqrt3 / 2) * Vy + (Wz * L)
        V3 = -0.5 * Vx + (sqrt3 / 2) * Vy + (Wz * L)
        return V1, V2, V3

    def update_odometry(self,x,y,theta,Vx,Vy,Wz,dt):
        dx = math.cos(theta) * Vx - math.sin(theta) * Vy
        dy = math.sin(theta) * Vx + math.cos(theta) * Vy

        x_new = x + dx * dt
        y_new = y + dy *dt 
        theta_new = theta + Wz * dt

        return (x_new,y_new,theta_new)

        
    def velocity_callback(self,msg):
        if len(msg.data) != 3:
            rospy.logwarn("🚨 Données incomplètes reçues, attendu 3 vitesses.")
            return

        v1, v2, v3 = msg.data

        # Log pour debug
        rospy.loginfo(f"📥 Vitesse roues reçues : V1={v1:.2f}, V2={v2:.2f}, V3={v3:.2f}")

        now = rospy.Time.now()
        dt = (now - self.last_time).to_sec()
        self.last_time = now

        # # Cinématique directe
        # Vx = -0.5 * v3 - 0.5 * v2 + v1
        # Vy = sqrt3 * (v3 - v2)
        # Wz = (v1 + v2 + v3) / L

        Vx,Vy,Wz = self.Kinematic_direct(v1,v2,v3)

        # Mise à jour odométrie
        dx = math.cos(self.theta) * Vx - math.sin(self.theta) * Vy
        dy = math.sin(self.theta) * Vx + math.cos(self.theta) * Vy

        self.x += dx * dt
        self.y += dy * dt
        self.theta += Wz * dt

        # Publication TF
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        q = tf.transformations.quaternion_from_euler(0, 0, self.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.odom_broadcaster.sendTransform(t)

        # Publication Odometry
        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        odom.twist.twist.linear.x = Vx
        odom.twist.twist.linear.y = Vy
        odom.twist.twist.angular.z = Wz

        self.odom_pub.publish(odom)


if __name__ == '__main__':
    try:
        OmniOdometry()
    except rospy.ROSInterruptException:
        pass