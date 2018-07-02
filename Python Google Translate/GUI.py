######################################################
## Author: ANIMIKH AICH (animikhaich@gmail.com)     ##
## 03 July 2018                                     ##
## Google Translate Using Python                    ##
## RNS Institute of Technology, Bengaluru, India    ##
######################################################

import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import GoogleTranslate_Selenium


class Window(QMainWindow, QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(450, 450, 800, 520)
        self.setWindowTitle('Translator')
        self.setWindowIcon(QIcon('./Assets/icon.png'))
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.exit_text = 'Exited Application'
        self.file_open_button = None
        self.quit_button = None
        self.textbox_input = None
        self.textbox_output = None
        self.output_label = None
        self.input_label = None
        self.file_text = None
        self.my_output = None
        self.my_text = None
        self.summarize_button = None
        self.n = None
        self.default_font = QFont("Arial", 14)
        self.num_lines = None
        self.language = None
        self.sent_num = None
        self.warning_text_1 = 'You have chosen summarization length more than the actual text length!\n' + \
                              'Please enter a valid number less than the length of actual text'

        self.init_ui()

    # main function containing all the buttons and other elements to display
    def init_ui(self):
        # The exit button on the right bottom corner
        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.exit_application)
        self.quit_button.resize(self.quit_button.minimumSizeHint())

        # The File Open button on the left bottom corner
        self.file_open_button = QPushButton('Open File', self)
        self.file_open_button.clicked.connect(self.file_open)
        self.file_open_button.resize(self.file_open_button.minimumSizeHint())

        # The Summarize button on the left bottom corner
        self.summarize_button = QPushButton('Translate', self)
        self.summarize_button.clicked.connect(self.translate_gui)
        self.summarize_button.resize(self.summarize_button.sizeHint())

        # Left Textbox element used to input the text to be summarized --- Editable
        self.textbox_input = QPlainTextEdit(self)
        self.textbox_input.setFont(self.default_font)

        # Right Textbox element used to display the output of the summarized text --- Not Editable (incomplete)
        self.textbox_output = QTextEdit(self)
        self.textbox_output.setFont(self.default_font)
        self.textbox_output.setReadOnly(True)

        # Textbox for the Number of lines to summarize to
        self.language = QLineEdit(self)

        # Left Textbox heading label
        self.input_label = QLabel(self, text='Input Text')
        new_font = QFont("Arial", 16, QFont.Bold)
        self.input_label.setFont(new_font)
        self.input_label.adjustSize()
        self.input_label.setAlignment(Qt.AlignCenter)

        # Right Textbox heading label
        self.output_label = QLabel(self, text='Output Text')
        new_font = QFont("Arial", 16, QFont.Bold)
        self.output_label.setFont(new_font)
        self.output_label.adjustSize()
        self.output_label.setAlignment(Qt.AlignCenter)

        # Font for the label stating the number of lines to summarize to
        self.num_lines = QLabel(self, text='Language:')
        new_font = QFont("Arial", 10)
        self.num_lines.setFont(new_font)

        # Setting the logo or picture in the middle
        pixmap = QPixmap(os.getcwd() + "./Assets/main.png").scaled(250, 250, Qt.KeepAspectRatio)
        pic = QLabel(self)
        pic.setPixmap(pixmap)
        pic.setAlignment(Qt.AlignCenter)

        # The layout for proper padding of the button
        summarize_pad_layout = QHBoxLayout()
        summarize_pad_layout.addStretch()
        summarize_pad_layout.addWidget(self.summarize_button)
        summarize_pad_layout.addStretch()

        # Layout for the input textbox which chooses the number of lines to be summarized to
        line_num_input_layout = QHBoxLayout()
        line_num_input_layout.addWidget(self.num_lines, alignment=Qt.AlignCenter)
        line_num_input_layout.addWidget(self.language, alignment=Qt.AlignHCenter)

        # Middle layout of the grid
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(pic)
        middle_layout.addLayout(summarize_pad_layout)
        middle_layout.addLayout(line_num_input_layout)

        # The main Grid Layout
        main_grid_layout = QGridLayout()
        main_grid_layout.addWidget(self.input_label, 0, 0)
        main_grid_layout.addWidget(self.output_label, 0, 2)
        main_grid_layout.addLayout(middle_layout, 1, 1)
        main_grid_layout.addWidget(self.textbox_input, 1, 0)
        main_grid_layout.addWidget(self.textbox_output, 1, 2)
        main_grid_layout.addWidget(self.file_open_button, 2, 0, alignment=Qt.AlignLeft)
        main_grid_layout.addWidget(self.quit_button, 2, 2, alignment=Qt.AlignRight)

        # Menu bar Commands start
        # Open file menu
        menu_open_file = QAction("&Open File", self)
        menu_open_file.setShortcut("Ctrl+O")
        menu_open_file.setStatusTip('Open from text file')
        menu_open_file.triggered.connect(self.file_open)

        # Save file menu
        menu_save_file = QAction("&Save File", self)
        menu_save_file.setShortcut("Ctrl+S")
        menu_save_file.setStatusTip('Save the out text')
        menu_save_file.triggered.connect(self.file_save)

        # Exit menu
        menu_exit = QAction("&Exit", self)
        menu_exit.setShortcut("Ctrl+Q")
        menu_exit.setStatusTip('Exit the program')
        menu_exit.triggered.connect(self.exit_application)

        # Font Choice for input textbox
        font_choice_input = QAction('&Input Font', self)
        font_choice_input.triggered.connect(self.input_font_choice)

        # Font Choice for output textbox
        font_choice_output = QAction('&Output Font', self)
        font_choice_output.triggered.connect(self.output_font_choice)

        self.statusBar()

        # The File menu option
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(menu_open_file)
        file_menu.addAction(menu_save_file)
        file_menu.addAction(menu_exit)

        # The Edit menu option
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&Edit')
        file_menu.addAction(font_choice_input)
        file_menu.addAction(font_choice_output)

        self.wid.setLayout(main_grid_layout)
        self.show()

    # Open file Function
    # Opens Dialog Box to open the file and select text
    # If file is of valid readable format, displays the contents on the left text box
    # Else throws a warning dialog box and prompts to either chose again else cancel
    def file_open(self):
        # noinspection PyBroadException
        try:
            name = QFileDialog.getOpenFileName(self, 'Open File')
            file = open(name[0], 'r')
            self.file_text = file.read()
            self.textbox_input.setPlainText(self.file_text)

            return self.file_text
        except Exception as e:
            print('Error Reported:', e)
            message_box = QMessageBox.warning(self, 'Error!', 'File Open Error! Please Choose Valid File!',
                                              QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                self.file_open()
            else:
                pass

    # Takes the input from the left textbox, summarize that and display on the right text box
    def translate_gui(self):
        # noinspection PyBroadException
        try:
            self.lang = self.language.text()
            self.my_text = self.textbox_input.toPlainText()
            self.my_output = GoogleTranslate_Selenium.translate(self.my_text, self.lang)
            self.textbox_output.setPlainText(self.my_output)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Error!', 'You have to input the text in the input textbox!\n'
                                                'You have to input a number in the number box!',
                                QMessageBox.Ok)

    # Exit Definition. Runs when the app is Quit using the 'Quit' button
    def exit_application(self):
        print(self.exit_text)
        sys.exit()

    # Reserve function for the selection box to have option to chose number of lines (unused)
    def selection_box(self):
        print('Inside selection_box')
        combo_box = QComboBox(self)
        for i in range(self.sent_num):
            item_text = str(i + 1) + ' Lines'
            combo_box.addItem(item_text)
        combo_box.move(365, 300)
        qApp.processEvents()

    # Font Selection for the input textbox
    def input_font_choice(self):
        font, ok = QFontDialog.getFont(self.textbox_input.font(), self)
        if ok:
            # QApplication.setFont(font)
            self.textbox_input.setFont(font)
            print("Display Fonts", font)

    # Font Selection for the output textbox
    def output_font_choice(self):
        font, ok = QFontDialog.getFont(self.textbox_output.font(), self)
        if ok:
            # QApplication.setFont(font)
            self.textbox_output.setFont(font)
            print("Display Fonts", font)

    # Saving the file function
    def file_save(self):
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File', '', '*.txt')
            file = open(name[0], 'w')
            text = self.textbox_output.toPlainText()
            file.write(text)
            file.close()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Error!', "You don't have any text to save!",
                                QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    # GUI.show()
    sys.exit(app.exec_())
