import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QLineEdit, QCheckBox, QDesktopWidget, 
                             QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from manga import Manga

# Home screen when first opening
class HomeScreen(QWidget):
    def __init__(self, stacked_widget, main_window): # Pass the stacked widget to HomeScreen for button functionality
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.title_label = QLabel("Welcome to Manga Tracker")
        self.new_collection_button = QPushButton("+ New Collection")
        self.view_collection_button = None # Will be created if there is manga data
        self.initUI()

    def initUI(self):
        # Layout
        vbox = QVBoxLayout()
        vbox.addStretch(1) # Adds space between widgets in the layout
        vbox.addWidget(self.title_label, alignment=Qt.AlignHCenter) # Set alignment
        vbox.addStretch(10)
        vbox.addWidget(self.new_collection_button)
        # Dynamically add the view collection button and hide the new collection button if there is manga data
        if self.main_window.mangas:
            self.view_collection_button = QPushButton("View Collection")
            vbox.addWidget(self.view_collection_button)
            self.view_collection_button.clicked.connect(self.view_collection)
            vbox.removeWidget(self.new_collection_button)
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
    
    def view_collection(self):
        # Refresh the collection screen table
        self.main_window.collection_screen.populate_table()
        self.stacked_widget.setCurrentIndex(2)

# Screen for adding new series to collection
class NewSeriesScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.title_label = QLabel("Add new series")
        self.name_label = QLabel("Name of Manga: ")
        self.name_lineedit = QLineEdit(self)
        self.artbook = QCheckBox("Check if art book or misc.")
        self.serializing_label = QLabel("Is series done serializing? ")
        self.serializing = QCheckBox()
        self.volumes_owned_label = QLabel("# of volumes owned: ")
        self.volumes_owned_lineedit = QLineEdit(self)
        self.total_volumes_label = QLabel("# of total volumes available: ")
        self.total_volumes_lineedit = QLineEdit(self)
        self.price_per_volume_label = QLabel("$ per volume: ")
        self.price_per_volume_lineedit = QLineEdit(self)
        self.submit = QPushButton("Submit")
        self.initUI()
    
    def initUI(self):
        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
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
        grid.addWidget(self.submit, 6, 1, alignment=Qt.AlignRight)
        self.setLayout(vbox)

        # Style Sheet
        self.submit.setMaximumWidth(200)
        self.setStyleSheet('''
            QLabel{
                font-size: 30px;
                font-weight: bold;
            }               
            QPushButton{
                font-size: 10px;
                font-family: calibri;
                padding: 15px 40px;
                margin: 25px;
                border: 3px solid;
                border-radius: 15px;
                background-color: hsl(136, 92%, 24%);
            }
            QPushButton:hover{
                background-color: hsl(136, 92%, 44%);
            }
        ''')
        
        # Submit Button Functionality
        self.submit.clicked.connect(self.on_click) 

    def on_click(self):
        # Create a Manga object based on what the user inputted when pressing submit
        print("clicked")
        # Set all arguments for Manga object to user input
        name = self.name_lineedit.text()
        volumes_owned_text = self.volumes_owned_lineedit.text()
        total_volumes_text = self.total_volumes_lineedit.text()
        price_per_volume_text = self.price_per_volume_lineedit.text()
        # Check all inputs are filled out
        if not name or not volumes_owned_text or not total_volumes_text or not price_per_volume_text:
            # Throw error
            print("Error: You have not filled out all requirements")
            QMessageBox.warning(self, "Missing Fields", "Please fill out all required fields")
            return
        # Convert data types plus error handling
        try:
            volumes_owned = int(self.volumes_owned_lineedit.text())
            total_volumes = int(self.total_volumes_lineedit.text())
            price_per_volume = float(self.price_per_volume_lineedit.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Make sure volumes are integers and price is a number.")
            print("Value error")
            return
        # Create manga object
        manga = Manga(
            title = self.name_lineedit.text(),
            volumes_owned = volumes_owned,
            total_volumes = total_volumes,
            price_per_volume = price_per_volume,
            is_serializing = self.serializing.isChecked(),
            is_misc = self.artbook.isChecked()
        )
        # Store manga in the dictionary using the title as the key
        self.main_window.mangas[manga.title] = manga
        self.main_window.save_mangas()
        # Rebuild collection screen and navigate to collection
        self.main_window.collection_screen.populate_table() 
        self.main_window.stacked_widget.setCurrentIndex(2) 


class CollectionScreen(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.title_label = QLabel("My Collection")
        self.new_series_button = QPushButton("+ Add New Series")
        # Add a table to hold collection data
        self.table = QTableWidget()
        self.initUI()
    
    def initUI(self):
        # Initialize table
        self.table.setColumnCount(5) # set the number of columns in table
        self.table.setHorizontalHeaderLabels(["Manga", "# of Volumes Owned", "# of Total Volumes Available", "$/Volume", "$/Series"]) # set column titles
        self.populate_table()
        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.new_series_button)
        self.new_series_button.clicked.connect(self.on_click)
        vbox.addWidget(self.table)
        self.setLayout(vbox)
    
    def populate_table(self):
        mangas = self.main_window.mangas
        # Clear table
        self.table.clearContents()
        self.table.setRowCount(len(mangas))
        # Loop through mangas and fill rows
        for row, manga in enumerate(mangas.values()):
            title_item = QTableWidgetItem(manga.title)
            volumes_owned_item = QTableWidgetItem(str(manga.volumes_owned))
            total_volumes_item = QTableWidgetItem(str(manga.total_volumes))
            price_per_volume_item = QTableWidgetItem(f"${manga.price_per_volume:.2f}")
            total_price_item = QTableWidgetItem(f"${manga.total_series_price:.2f}")     

            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, volumes_owned_item)
            self.table.setItem(row, 2, total_volumes_item)
            self.table.setItem(row, 3, price_per_volume_item)
            self.table.setItem(row, 4, total_price_item)
        # Add summary row for totals
        # Find row count
        row_count = self.table.rowCount()
        # Insert 3 rows, 1 blank, 1 for titles (row_count + 1), 1 for totals (row_count + 2)
        self.table.insertRow(row_count)
        self.table.insertRow(row_count)
        self.table.insertRow(row_count)
        # Set titles
        total_vols_title = QTableWidgetItem("Total # of Volumes")
        total_series_title = QTableWidgetItem("Total # of Series'")
        total_money_title = QTableWidgetItem("Total $ of Collection")
        # Set Totals
        total_series = QTableWidgetItem(str(Manga.get_total_series_collection_count()))
        total_volumes = QTableWidgetItem(str(Manga.get_total_volume_collection_count()))
        total_price = QTableWidgetItem(f"${Manga.get_total_collection_price():.2f}")    
        # Insert Titles
        self.table.setItem(row_count + 1, 0, total_series_title)
        self.table.setItem(row_count + 1, 2, total_vols_title)
        self.table.setItem(row_count + 1, 4, total_money_title)
        # Insert Totals
        self.table.setItem(row_count + 2, 0, total_series)
        self.table.setItem(row_count + 2, 2, total_volumes)
        self.table.setItem(row_count + 2, 4, total_price)
        # Make columns resize
        self.table.resizeColumnsToContents()

    def on_click(self):
        self.stacked_widget.setCurrentIndex(1)

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
        
        # Set dictionary to hold manga objects
        self.mangas = {}
        self.data_file = "mangas.json"
        self.load_mangas()

        # Create a stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()
        
        # Create screens
        self.home_screen = HomeScreen(self.stacked_widget, self)
        self.new_series_screen = NewSeriesScreen(self)
        self.collection_screen = CollectionScreen(self.stacked_widget, self)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.new_series_screen)
        self.stacked_widget.addWidget(self.collection_screen)
        
        # Set the stacked widget as the central widget
        self.setCentralWidget(self.stacked_widget)
    
    def save_mangas(self):
        # Conver Manga objects to dictionaries for JSON
        data = {title: {
            "title": manga.title,
            "volumes_owned": manga.volumes_owned,
            "total_volumes": manga.total_volumes,
            "price_per_volume": manga.price_per_volume,
            "is_serializing": manga.is_serializing,
            "is_misc": manga.is_misc
        } for title, manga in self.mangas.items()}
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)    
    
    def load_mangas(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                for title, info in data.items():
                    self.mangas[title] = Manga(
                        title=info["title"],
                        volumes_owned=info["volumes_owned"],
                        total_volumes=info["total_volumes"],
                        price_per_volume=info["price_per_volume"],
                        is_serializing=info["is_serializing"],
                        is_misc=info["is_misc"]
                    )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()