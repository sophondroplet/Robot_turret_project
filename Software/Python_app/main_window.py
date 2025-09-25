from PyQt6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from PyQt6.QtCore import Qt, QSize

import camera
import settings_menu
import controls 
import serial_manager

class MainWindow(QMainWindow):
    cam = None
    cam_index = 0
    cam_running = False
    layout = QStackedLayout()
    settings_frame = None

    controls_widget = None

    sm = None
    
    def __init__(self):
        super().__init__()

        self.sm = serial_manager.SerialManager()

        self.settings_frame = settings_menu.SettingsMenu(self.sm)
        self.settings_frame.start_button.clicked.connect(self.update_settings)

        self.setWindowTitle("Turret Control")
        self.cam = camera.Camera(self.cam_index)

        self.controls_widget = controls.Controls()

        self.layout.setStackingMode(QStackedLayout.StackingMode.StackOne)
        self.layout.addWidget(self.settings_frame.widget)
        self.layout.addWidget(self.cam.c_frame)
        self.layout.addWidget(self.controls_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        
    def loop(self):
        # "X(int:x(0-180))Y(int:y(0-180))Z(int:z(0-180))S(bool:slow)F(bool:fast)R(bool:on/off)"
    
        if not self.cam_running:
             return
             
        self.cam.display_camera()
        self.controls_widget.update()
        command = "X{0}Y{1}Z{2}S{3}F{4}R{5}\n".format(self.controls_widget.x_pos, self.controls_widget.y_pos, self.controls_widget.z_pos, int(self.controls_widget.box.shoot), int(self.controls_widget.box.charge), int(self.controls_widget.reload_mode))
        self.sm.communicate(command)
            
        
            

    # def resizeEvent(self, e):
    #     if self.frameGeometry().width() >= 1920 and self.frameGeometry().height() >= 1080:
    #         self.cam.update_size(1920,1080)
    #     elif self.frameGeometry().width() < 1920 or self.frameGeometry().height() < 1080:
    #         self.cam.update_size(1280,720)
    
    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key.Key_Escape and self.cam_running:
            self.cam_running = not self.cam_running
            self.setFixedSize(QSize(640,480))
            self.cam.disconnect_camera()
            self.sm.close()
            self.layout.setStackingMode(QStackedLayout.StackingMode.StackOne)
            print(self.layout.currentIndex())
        elif e.key() == Qt.Key.Key_R and self.cam_running:
            self.controls_widget.reload_mode = not self.controls_widget.reload_mode
        else:
            self.controls_widget.box.controlsKeyPressHandler(e.key())
            
    def keyReleaseEvent(self, e) -> None:
        if e.isAutoRepeat():
            return
        self.controls_widget.box.controlsKeyReleaseHandler(e.key())
    
    
    def update_settings(self):
        if self.cam.camera:
            self.cam.disconnect_camera()
        
        new_resolution_settings = self.settings_frame.get_resolution_setting()
        new_resolution_settings_list = new_resolution_settings.split(',')
        self.cam.update_size(int(new_resolution_settings_list[0]), int(new_resolution_settings_list[1]))

        if not self.cam.connect_camera(self.settings_frame.get_camera_setting()):
            return
        
        self.setFixedSize(QSize(int(new_resolution_settings_list[0]), int(new_resolution_settings_list[1])))

        if not self.sm.start(self.settings_frame.get_port_setting()):
            return


        self.layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        
        self.cam_running = not self.cam_running