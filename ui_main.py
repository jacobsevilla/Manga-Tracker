import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QLineEdit, QCheckBox, QDesktopWidget)
from PyQt5.QtCore import Qt

# Home screen when first opening
class HomeScreen(QWidget):
    def __init__(self, stacked_widget): # Pass the stacked widget to HomeScreen for button functionality
        super().__init__()
        self.stacked_widget = stacked_widget
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
                font-family: calibri;
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
        self.new_collection_button.clicked.connect(self.on_click) # Switches to the new series widget in the stacked widget
    
    def on_click(self):
        self.stacked_widget.setCurrentIndex(1)
        print("clicked")

class NewSeriesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Add new series")
        self.name_label = QLabel("Name of Manga: ")
        self.name_lineedit = QLineEdit(self)
        self.artbook = QCheckBox("Check if art book or misc.")
        self.serializing_label = QLabel("Is series done serializing? ")
        self.serializing = QCheckBox()
        self.volumes_owned_label = QLabel("# of volumes owned: ")
        self.volumes_owned_lineedit = QLineEdit(self)
        self.total_volumes_label = QLabel("# of total volumes: ")
        self.total_volumes_lineedit = QLineEdit(self)
        self.price_per_volume_label = QLabel("$ per volume: ")
        self.price_per_volume_lineedit = QLineEdit(self)
        self.submit = QPushButton("Submit")
        self.initUI()
    
    def initUI(self):
        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        grid = QGridLayout()
        vbox.addLayout(grid)
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_lineedit, 0, 1)
        grid.addWidget(self.artbook, 1, 0)
        grid.addWidget(self.serializing_label, 2, 0)
        grid.addWidget(self.serializing, 2, 1)
        grid.addWidget(self.volumes_owned_label, 3, 0)
        grid.addWidget(self.volumes_owned_lineedit, 3, 1)
        grid.addWidget(self.total_volumes_label, 4, 0)
        grid.addWidget(self.total_volumes_lineedit, 4, 1)
        grid.addWidget(self.price_per_volume_label, 5, 0)
        grid.addWidget(self.price_per_volume_lineedit, 5, 1)
        grid.addWidget(self.submit, 6, 1)
        self.setLayout(vbox)

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
        self.home_screen = HomeScreen(self.stacked_widget)
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