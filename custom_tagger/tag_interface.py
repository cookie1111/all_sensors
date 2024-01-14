import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import tag_backend 

class ButtonCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.created_buttons = {}
        self.created_streams = {}
        self.buttons_pressed = {}
        self.button_grid_layout = QGridLayout()
        self.initUI()
        
        self.current_row = 0
        self.current_column = 0
        self.max_columns = 8
        

    def initUI(self):
        self.setWindowTitle('PyQt Button Creator')
        self.setGeometry(300, 300, 250, 180)

        # Layout
        main_vbox = QVBoxLayout()

        top_hbox = QHBoxLayout()
        self.text_field = QLineEdit(self)
        self.text_field.setPlaceholderText("Type button name")
        top_hbox.addWidget(self.text_field)

        # Create button
        self.create_button = QPushButton('Create', self)
        self.create_button.clicked.connect(self.createButton)
        top_hbox.addWidget(self.create_button)

        # setup stream button
        self.stream_button = QPushButton('Start', self)
        self.stream_button.clicked.connect(self.createStreams)
        top_hbox.addWidget(self.stream_button)

        main_vbox.addLayout(top_hbox)

        self.button_grid_layout.setSpacing(10)
        main_vbox.addLayout(self.button_grid_layout)

        self.setLayout(main_vbox)

    def createButton(self):
        button_name = self.text_field.text()
        
        if button_name and button_name not in self.created_buttons.keys():
            # Limit the number of buttons to 64
            if len(self.created_buttons) < 64:
                new_button = QPushButton(button_name, self)
                new_button.setCheckable(True)
                new_button.clicked.connect(self.buttonClicked)
                new_button.setStyleSheet("background-color : lightgrey")
                self.buttons_pressed[button_name] = 0

                button_size = 50#(self.width() // self.max_columns) - 10
                new_button.setFixedSize(button_size,button_size)

                self.button_grid_layout.addWidget(new_button,self.current_row,self.current_column)
                self.text_field.clear()
                self.created_buttons[button_name] = new_button

                self.current_column += 1
                if self.current_column >= self.max_columns:
                    self.current_row +=1
                    self.current_column = 0
            else:
                print("Maximum button limit reached.")
        else:
            print("Button name cannot be empty or be named the same as any other buttons.")

    def sendLSLData(self):
        for button in self.buttons_pressed:
            tag_backend.stream(button,self.buttons_pressed[button])

    def createStreams(self):
        print(f"Creating LSL streams for:")
        tag_backend.prepare_LSL_streaming(list(self.created_buttons.keys()))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.sendLSLData)
        self.timer.start(500)
        

    def buttonClicked(self):
        clicked_button = self.sender()
        
        # if button is checked
        if clicked_button.isChecked():
 
            # setting background color to light-blue
            clicked_button.setStyleSheet("background-color : lightblue")
            self.buttons_pressed[clicked_button.text()] = 1
 
        # if it is unchecked
        else:
 
            # set background color back to light-grey
            clicked_button.setStyleSheet("background-color : lightgrey")
            self.buttons_pressed[clicked_button.text()] = 0


    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.createButton()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    ex = ButtonCreator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
