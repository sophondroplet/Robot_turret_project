from PyQt6.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SettingsMenu():
    layout = QGridLayout()
    widget = None
    camera = None
    resolution = None
    start_button = None
    port = None
    sm = None
    list_of_ports = None

    def __init__(self, sm):
        self.sm = sm
        #sp = QSizePolicy.Policy.Expanding
        font = QFont('Arial', 15)
        self.camera = QComboBox()
        self.camera.addItems(['0','1','2','3'])
        #self.camera.setSizePolicy(sp,sp)
        self.camera.setMinimumSize(200,50)
        self.camera.setFont(font)

        self.resolution = QComboBox()
        self.resolution.addItems(['640,480','1280,720','1920,1080'])
        #self.resolution.setSizePolicy(sp, sp)
        self.resolution.setMinimumSize(200,50)
        self.resolution.setFont(font)

        self.port = QComboBox()
        #self.port.addItems(['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12'])
        self.port.addItems(sm.get_ports())
        self.port.setMinimumSize(200,50)
        self.port.setFont(font)

        camera_label = QLabel("Camera:")
        camera_label.setFont(font)
        self.layout.addWidget(camera_label, 0, 0)
        self.layout.addWidget(self.camera, 0, 1)

        resolution_label = QLabel("Resolution:")
        resolution_label.setFont(font)
        self.layout.addWidget(resolution_label, 1,0)
        self.layout.addWidget(self.resolution, 1, 1)
        
        port_label = QLabel("Port:")
        port_label.setFont(font)
        self.layout.addWidget(port_label, 2, 0)
        self.layout.addWidget(self.port, 2, 1)

        self.start_button = QPushButton("Start")
        self.layout.addWidget(self.start_button, 3, 0, 1, 2)
        #self.start_button.setSizePolicy(sp,sp)
        self.start_button.setMinimumSize(200,50)
        self.start_button.setFont(font)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.widget = QWidget()
        self.widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        #self.widget.setStyleSheet("background-color: rgba(255,254,247,255)")
        self.widget.setStyleSheet("QWidget {background-color: rgb(255, 254, 247)} QComboBox {background-color: white} QPushButton {background-color: white}")
        self.widget.setLayout(self.layout)
        
    def get_camera_setting(self):
        return self.camera.currentIndex()

    def get_resolution_setting(self):
        return self.resolution.currentText()
    def get_port_setting(self):
        return self.port.currentText()


    
    
    



