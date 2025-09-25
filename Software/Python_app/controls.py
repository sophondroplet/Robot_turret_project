from PyQt6.QtWidgets import QWidget, QStackedLayout, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import Qt, QPoint
import control_box

class Controls(QWidget):
    
    width = 640
    height = 480
    init_x_pos = 90
    init_y_pos = 90
    init_z_pos = 100
    x_pos = init_x_pos
    y_pos = init_y_pos
    z_pos = init_z_pos
    reload_mode = False

    box = None
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.box = control_box.ControlBox(self)
        
        layout = QGridLayout()
        #layout.addWidget(control_box.ControlBox())
        
        layout.addWidget(self.box)
        #self.box.pos = (QPoint(self.width//2-50, self.height//2-50))
        #layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #layout.setCurrentIndex(0)
        self.setLayout(layout)
        self.setCursor(Qt.CursorShape.BlankCursor)


    def update_pos(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def update_size(self, width, height):
        self.width = width
        self.height = height
    
    def update(self):
        if self.box.up_press and self.z_pos < 120:
            self.z_pos += 2
        elif self.box.down_press and self.z_pos > 0:
            self.z_pos -= 2
        
        