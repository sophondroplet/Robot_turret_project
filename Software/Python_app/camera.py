from PyQt6.QtWidgets import QLabel, QMessageBox
from PyQt6.QtGui import QPixmap, QColor, QImage
from PyQt6.QtCore import Qt

import cv2 as cv

class Camera:
    camera_size = [1280, 720]
    c_frame = None
    camera = None

    def __init__(self,cam_num):
        self.c_frame = QLabel()
        self.c_frame.setPixmap(QPixmap(640,480))
        self.c_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
    def connect_camera(self, cam_num):
        self.camera = cv.VideoCapture(cam_num)
        if not self.camera.isOpened() or self.camera is None:
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setText("Failed to open camera.")
            message.exec()
            return False
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, self.camera_size[0])
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, self.camera_size[1])
        self.camera.set(cv.CAP_PROP_FPS, 60)
        return True
    
    def display_camera(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Error reading frame")
            return
        self.c_frame.setPixmap(QPixmap.fromImage(self.convert_to_qt(frame)))
        
    # def pause_camera(self):
    #     self.c_frame.setPixmap(QPixmap(0,0))

    def disconnect_camera(self):
        self.camera.release()

    def convert_to_qt(self, cv_frame):
        height, width, channel = cv_frame.shape
        bytesPerLine = 3 * width
        qt_frame = QImage(cv_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888).rgbSwapped()
        
        return qt_frame.scaled(self.camera_size[0],self.camera_size[1],Qt.AspectRatioMode.KeepAspectRatio)
        
        
    def update_size(self, width, height):
        self.camera_size[0] = width
        self.camera_size[1] = height
        
        print(self.camera_size)
        
