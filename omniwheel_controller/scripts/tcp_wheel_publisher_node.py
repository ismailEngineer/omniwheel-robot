#!/usr/bin/env python3
import rospy
import socket
from std_msgs.msg import Float32MultiArray

def tcp_wheel_publisher():
    rospy.init_node('tcp_wheel_publisher_node')

    RASPBERRY_IP = rospy.get_param("~raspberry_ip", "192.168.1.167")
    PORT = rospy.get_param("~port", 5000)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((RASPBERRY_IP, PORT))
        rospy.loginfo(f"✅ Connecté à {RASPBERRY_IP}:{PORT}")
    except Exception as e:
        rospy.logerr(f"❌ Erreur de connexion : {e}")
        return

    pub = rospy.Publisher('/wheel_velocities', Float32MultiArray, queue_size=10)
    buffer = ""

    try:
        while not rospy.is_shutdown():
            chunk = client_socket.recv(1024).decode()
            if not chunk:
                break
            buffer += chunk

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    _, v1, v2, v3 = map(float, line.strip().split(","))
                    msg = Float32MultiArray()
                    msg.data = [v1, v2, v3]
                    pub.publish(msg)
                    rospy.loginfo(f"📡 V1={v1:.2f}, V2={v2:.2f}, V3={v3:.2f}")
                except ValueError:
                    rospy.logwarn(f"⚠️ Ligne ignorée (mauvais format) : {line}")
                    continue
    except KeyboardInterrupt:
        rospy.loginfo("⛔ Déconnexion...")
    finally:
        client_socket.close()

if __name__ == '__main__':
    try:
        tcp_wheel_publisher()
    except rospy.ROSInterruptException:
        pass
