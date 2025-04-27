import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoystickControlNode(Node):
    def __init__(self):
        super().__init__('joystick_control_node')
        
        # Publisher untuk cmd_vel (kontrol gerakan robot)
        self.publisher_ = self.create_publisher(Twist, '/model/vehicle_blue/cmd_vel', 10)
        
        
        # Subscriber untuk joystick input
        self.joy_subscriber_ = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        # Inisialisasi nilai Twist
        self.twist_ = Twist()
        # self.twist_.linear.x = 0.1
        # self.publisher_.publish(self.twist_)

        self.get_logger().info('JoystickControlNode telah dimulai!')
    
    def joy_callback(self, msg):
        # Membaca input dari joystick (axes dan buttons)
        axes = msg.axes  # Nilai analog dari stick
        buttons = msg.buttons  # Status tombol

        # Log nilai-nilai joystick
        self.get_logger().info(f'Axes: {axes}, Buttons: {buttons}')

        # Memperbarui perintah Twist berdasarkan input joystick
        self.twist_.linear.x = axes[1] # Menggerakkan maju/mundur dengan analog stick kiri
        self.twist_.angular.z = axes[3]  # Memutar robot dengan analog stick kanan

        # # Menyusun kontrol gerakan berdasarkan tombol (misalnya tombol 0 untuk berhenti)
        # if buttons[0] == 1:  # Jika tombol 0 ditekan
        #     self.twist_.linear.x = 0.0  # Hentikan gerakan maju/mundur
        #     self.twist_.angular.z = 0.0  # Hentikan rotasi

        # Publikasikan perintah gerakan (Twist) ke topik cmd_vel
        self.publisher_.publish(self.twist_)

def main(args=None):
    # Inisialisasi ROS2 dan node
    rclpy.init(args=args)
    node = JoystickControlNode()

    # Menjalankan node sampai diberhentikan
    rclpy.spin(node)

    # Menutup node setelah selesai
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
