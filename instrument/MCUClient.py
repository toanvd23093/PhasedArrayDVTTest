import numpy as np
import socket

class MCUClient:
    def __init__(self, ip_address, port, num_points_fast_arm, num_points_slow_arm):
        self.length_x = 482.6  # mm
        self.length_y = 482.6  # mm
        self.cir_of_pulley = 111.8  # mm

        self.num_points_fast_arm = num_points_fast_arm
        self.num_points_slow_arm = num_points_slow_arm

        self.mcu_ip = ip_address
        self.port = port

        self.__setup_motors_params()
        
    def move_motors(self,X,Y):
        self.__send_to_tcp_server(bytes([X, Y]))

    def __setup_motors_params(self):
        self.delta_x = round(self.length_x / (self.num_points_fast_arm - 1))
        self.delta_y = round(self.length_y / (self.num_points_slow_arm - 1))

        self.step_length_x = round(self.length_x * 3200 / self.cir_of_pulley)
        self.step_length_y = round(self.length_y * 3200 / self.cir_of_pulley)

        self.step_delta_x = round(self.step_length_x / (self.num_points_fast_arm - 1))
        self.step_delta_y = round(self.step_length_y / (self.num_points_slow_arm - 1))

        steps = [self.step_delta_x, self.step_delta_y]
        data = []

        for step in steps:
            step_cast = np.uint32(step)
            data.append((step_cast >> 24) & 0xFF)
            data.append((step_cast >> 16) & 0xFF)
            data.append((step_cast >> 8) & 0xFF)
            data.append(step_cast & 0xFF)

        self.__send_to_tcp_server(bytes(data))

    def __send_to_tcp_server(self,data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.mcu_ip, self.port))
            sock.sendall(data)