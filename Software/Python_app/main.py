import main_window
import camera
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

class App(QApplication):
    app = None
    window = None

    def __init__(self):
        self.app = super().__init__([])
        self.window = main_window.MainWindow()

    

if __name__ == '__main__':
    app = App() 
    app.window.show()
    timer = QTimer()
    def timerEvent():
        app.window.loop()
    timer.timeout.connect(timerEvent)
    timer.start(1000//60)
    app.exec()




