import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QLineEdit, QCheckBox)

# Home screen when first opening
class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Welcome to Manga Tracker!")
        self.new_collection_button = QPushButton("+ New Collection")
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        self.setLayout(vbox)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manga Tracker")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()
        
        # Create home screen
        self.home_screen = HomeScreen()
        
        # Add home screen to stacked widget
        self.stacked_widget.addWidget(self.home_screen)
        
        # Set the stacked widget as the central widget
        self.setCentralWidget(self.stacked_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()