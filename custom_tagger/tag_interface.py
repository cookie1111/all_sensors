import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit

class ButtonCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.created_buttons = {}
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('PyQt Button Creator')
        self.setGeometry(300, 300, 250, 180)

        # Layout
        self.vbox = QVBoxLayout()

        # Text field
        self.text_field = QLineEdit(self)
        self.text_field.setPlaceholderText("Type button name")
        self.vbox.addWidget(self.text_field)

        # Create button
        self.create_button = QPushButton('Create', self)
        self.create_button.clicked.connect(self.createButton)
        self.vbox.addWidget(self.create_button)

        self.setLayout(self.vbox)

    def createButton(self):
        button_name = self.text_field.text()
        
        if button_name:
            # Limit the number of buttons to 64
            if len(self.vbox.children()) <= 65:
                new_button = QPushButton(button_name, self)
                self.vbox.addWidget(new_button)
            else:
                print("Maximum button limit reached.")
        else:
            print("Button name cannot be empty.")
        self.created_buttons = 

def main():
    app = QApplication(sys.argv)
    ex = ButtonCreator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
