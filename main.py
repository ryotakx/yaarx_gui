import sys
import tools
from config import choice_list, parameter_dict, input_types, description
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QTextBrowser
from PyQt5.QtGui import QIntValidator, QValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp


hex_validator = QRegExpValidator(QRegExp('[0-9a-fA-F]{1,8}'))
decimal_validator = QIntValidator(0, 2147483647)
binary_validator = QRegExpValidator(QRegExp('[01]{1,16}'))
validators = {'hex': hex_validator, 'decimal': decimal_validator, 'binary': binary_validator}


class Demo(QWidget):

    def __init__(self):
        super(Demo, self).__init__()

        self.program_label = QLabel('Program:', self)
        self.program_combobox = QComboBox(self)
        self.description = QTextBrowser(self)
        self.description.setFixedHeight(80)
        self.da_label = QLabel('da:', self)
        self.db_label = QLabel('db:', self)
        self.dc_label = QLabel('dc:', self)
        self.da_line = QLineEdit(self)
        self.db_line = QLineEdit(self)
        self.dc_line = QLineEdit(self)
        self.da_line.setText('0')
        self.db_line.setText('0')
        self.dc_line.setText('0')
        self.da_line.setValidator(hex_validator)
        self.db_line.setValidator(hex_validator)
        self.dc_line.setValidator(hex_validator)
        self.da_combobox = QComboBox(self)
        self.db_combobox = QComboBox(self)
        self.dc_combobox = QComboBox(self)

        self.compute_button = QPushButton('compute', self)
        self.compute_button.clicked.connect(self.compute_func)

        self.text_browser = QTextBrowser(self)

        self.program_grid_layout = QGridLayout()
        self.grid_layout = QGridLayout()

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.layout_init()
        self.program_combobox_init()
        self.input_combobox_init()

    def layout_init(self):
        self.program_grid_layout.addWidget(self.program_label, 0, 0, 1, 1)
        self.program_grid_layout.addWidget(self.program_combobox, 0, 1, 1, 1)

        self.grid_layout.addWidget(self.da_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.da_combobox, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.da_line, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.db_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.db_combobox, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.db_line, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.dc_label, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.dc_combobox, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.dc_line, 2, 2, 1, 1)

        self.v_layout.addLayout(self.program_grid_layout)
        self.v_layout.addWidget(self.description)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addWidget(self.compute_button)
        self.v_layout.addWidget(self.text_browser)

        self.setLayout(self.v_layout)

    def program_combobox_init(self):
        self.program_combobox.addItems(choice_list)
        self.description.setText(description[self.program_combobox.currentText()])
        # self.on_combobox_change_layout()
        self.program_combobox.currentIndexChanged.connect(self.on_combobox_change_layout)
    #    self.program_combobox.currentIndexChanged.connect(lambda: self.on_combobox_func(self.program_combobox))

    #def on_combobox_func(self, combobox):
    #    if combobox == self.program_combobox:
    #        QMessageBox.information(self, 'Program_Combobox',
    #                                '{}: {}'.format(combobox.currentIndex(), combobox.currentText()))

    def input_combobox_init(self):
        self.da_combobox.addItems(input_types)
        self.db_combobox.addItems(input_types)
        self.dc_combobox.addItems(input_types)
        self.da_combobox.currentIndexChanged.connect(self.on_combobox_change_type)
        self.db_combobox.currentIndexChanged.connect(self.on_combobox_change_type)
        self.dc_combobox.currentIndexChanged.connect(self.on_combobox_change_type)

    def on_combobox_change_type(self):
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QComboBox):
                edit_line = self.grid_layout.itemAt(i+1).widget()
                edit_line.setValidator(validators[widget.currentText()])
                print(widget.currentText())

    def on_combobox_change_layout(self):
        program_name = self.program_combobox.currentText()
        self.description.setText(description[program_name])
        self.text_browser.clear()
        param_list = parameter_dict[program_name]
        for i in range(self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().deleteLater()
        for line_number, param in enumerate(param_list):
            self.grid_layout.addWidget(QLabel(param + ':', self), line_number, 0, 1, 1)
            combobox = QComboBox(self)
            combobox.addItems(input_types)
            combobox.currentIndexChanged.connect(self.on_combobox_change_type)
            self.grid_layout.addWidget(combobox, line_number, 1, 1, 1)
            line_edit = QLineEdit(self)
            line_edit.setText('0')
            line_edit.setValidator(hex_validator)
            self.grid_layout.addWidget(line_edit, line_number, 2, 1, 1)

    def input_validator(self):
        for i in range(self.grid_layout.count()):
            wig = self.grid_layout.itemAt(i).widget()
            if isinstance(wig, QLineEdit):
                print(wig.text())

    def compute_func(self):
        input_list = []
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                input_type = self.grid_layout.itemAt(i-1).widget().currentText()
                input_list.append((input_type, widget.text()))

        _, result, result_regex = tools.compute(self.program_combobox.currentText(), *tools.conversion(input_list))
        if result_regex:
            result = result + '\n\n=' + result_regex
        self.set_result_func(result)

    def set_result_func(self, result):
        self.text_browser.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())