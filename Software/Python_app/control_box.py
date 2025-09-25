import math

from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QGridLayout
from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QCursor, QPainter, QPixmap, QBrush

import mouse
import controls
# x 0 - 180 init 90
# y 0 - 125 init 90
# z 0 - 120 init 100
class ControlBox(QFrame):
    box_width = 400
    box_height = 400
    servo_x_pos = 0
    servo_y_pos = 0
    #servo_z_pos = 0
    x_middle = box_width // 2
    y_middle = box_height // 2
    box_x_pos = x_middle
    box_y_pos = y_middle
    center = None
    main_controls = None

    charge = False
    shoot = False

    up_press = False
    down_press = False

    real_to_servo_ratio = 10 / 40

    def __init__(self, c):
        super().__init__()
        
        self.main_controls = c
        self.servo_x_pos = self.main_controls.x_pos
        self.servo_y_pos = self.main_controls.y_pos

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFixedSize(self.box_width, self.box_height)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(0)

        self.setMouseTracking(True)
        
    
    # def get_pos(self,e):
    #     return e.x(), e.y()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(Qt.GlobalColor.green, Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(QPoint(self.x_middle, self.y_middle), 5, 5)

    def mouseMoveEvent(self, e):
        #QCursor.setPos(self.mapToGlobal(QPoint(self.box_width // 2, self.box_height // 2)))

        x_change = e.position().x() - self.box_x_pos
        if(self.servo_x_pos + int(x_change * self.real_to_servo_ratio) < 0):
            self.servo_x_pos = 0
        elif(self.servo_x_pos + int(x_change * self.real_to_servo_ratio) > 180):
            self.servo_x_pos = 180
        else:
            self.servo_x_pos += int(x_change * self.real_to_servo_ratio)
        self.box_x_pos += x_change

        y_change = e.position().y() - self.box_y_pos
        if(self.servo_y_pos + int(y_change * self.real_to_servo_ratio) < 0):
            self.servo_y_pos = 0
        elif(self.servo_y_pos + int(y_change * self.real_to_servo_ratio) > 125):
            self.servo_y_pos = 125
        else:
            self.servo_y_pos += int(y_change * self.real_to_servo_ratio)
        self.box_y_pos += y_change
        
        self.main_controls.update_pos(self.servo_x_pos, self.servo_y_pos)

    def leaveEvent(self, e) -> None:
        self.box_x_pos = self.x_middle
        self.box_y_pos = self.y_middle
        QCursor.setPos(self.mapToGlobal(QPoint(self.box_width // 2, self.box_height // 2)))
    
    def mousePressEvent(self, e):
        if(e.button() == Qt.MouseButton.RightButton):
            self.charge = True
        if(self.charge and e.button() == Qt.MouseButton.LeftButton):
            self.shoot = True
    
    def mouseReleaseEvent(self, e) -> None:
        if(mouse.is_pressed('right')):
            self.shoot = False
        elif(mouse.is_pressed('left')):
            self.charge = False
        else:
            self.shoot = False
            self.charge = False

    # def keyPressEvent(self, e) -> None:
    #     if(e.key() == Qt.Key.Key_Space):
    #         self.servo_z_pos += 10
    #     elif(e.key() == Qt.Key.Key_Shift):
    #         self.servo_z_pos -= 10
    #     self.main_controls.update_pos(self.servo_x_pos, self.servo_y_pos, self.servo_z_pos)
    
    def controlsKeyPressHandler(self, key):
        if(key == Qt.Key.Key_W and self.up_press == False):
            self.up_press = True
            print("up")
        elif(key == Qt.Key.Key_S and self.down_press == False):
            self.down_press = True
            print("down")

    def controlsKeyReleaseHandler(self, key):
        if(key == Qt.Key.Key_W):
            self.up_press = False
            print("up_release")
        elif(key == Qt.Key.Key_S):
            self.down_press = False
            print("down_release")


    
        

