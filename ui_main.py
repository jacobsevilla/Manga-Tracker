import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QLineEdit, QCheckBox, QDesktopWidget)
from PyQt5.QtCore import Qt

# Home screen when first opening
class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Welcome to Manga Tracker")
        self.new_collection_button = QPushButton("+ New Collection")
        self.initUI()

    def initUI(self):
        # Layout
        vbox = QVBoxLayout()
        vbox.addStretch(1) # Adds space between widgets in the layout
        vbox.addWidget(self.title_label, alignment=Qt.AlignHCenter) # Set alignment
        vbox.addStretch(10)
        vbox.addWidget(self.new_collection_button)
        self.setLayout(vbox)

        # Style Sheet
        self.setStyleSheet('''
            QLabel{
                font-size: 30px;
                font-weight: bold;
            }               
            QPushButton{
                font-size: 20px;
                font-family: Calibri;
                padding: 15px 40px;
                margin: 25px;
                border: 3px solid;
                border-radius: 15px;
                background-color: hsl(4, 0%, 50%);
            }
            QPushButton:hover{
                background-color: hsl(4, 0%, 70%);
            }
        ''')

        # New Collection Button Functionality
        self.new_collection_button.clicked.connect(self.on_click)
    
    def on_click(self):
        print("clicked")

class NewSeriesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Add new series")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manga Tracker")
        self.setGeometry(0, 0, 1400, 600)
        # Center the window by screen resolution
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        # Create a stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()
        
        # Create screens
        self.home_screen = HomeScreen()
        self.new_series_screen = NewSeriesScreen()
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.new_series_screen)
        
        # Set the stacked widget as the central widget
        self.setCentralWidget(self.stacked_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()