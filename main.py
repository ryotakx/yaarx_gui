import sys
import tools
from tools import validator_equal_to, input_validator, configs
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QTextBrowser
from PyQt5.QtGui import QIcon


class Demo(QWidget):

    def __init__(self):
        super(Demo, self).__init__()
        self.setWindowTitle(configs.window_title)
        self.setWindowIcon(QIcon(configs.window_logo))
        self.word_size_label = QLabel('Word Size', self)
        self.program_label = QLabel('Program:', self)
        self.program_combobox = QComboBox(self)
        self.word_size_combobox = QComboBox(self)
        self.current_program = None
        self.word_size = configs.word_size_list[0]
        self.description = QTextBrowser(self)
        self.description.setFixedHeight(80)

        self.compute_button = QPushButton('compute', self)
        self.compute_button.clicked.connect(self.compute_func)

        self.text_browser = QTextBrowser(self)

        self.program_grid_layout = QGridLayout()
        self.grid_layout = QGridLayout()

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.layout_init()
        self.word_size_combobox_init()
        self.program_combobox_init()
        self.grid_layout_init()

    def layout_init(self):
        self.program_grid_layout.addWidget(self.program_label, 0, 0, 1, 1)
        self.program_grid_layout.addWidget(self.program_combobox, 0, 1, 1, 1)
        self.program_grid_layout.addWidget(self.word_size_label, 1, 0, 1, 1)
        self.program_grid_layout.addWidget(self.word_size_combobox, 1, 1, 1, 1)

        self.v_layout.addLayout(self.program_grid_layout)
        self.v_layout.addWidget(self.description)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addWidget(self.compute_button)
        self.v_layout.addWidget(self.text_browser)

        self.setLayout(self.v_layout)

    def grid_layout_init(self):
        self.on_combobox_change_layout()

    def word_size_combobox_init(self):
        self.word_size_combobox.addItems([str(i) for i in configs.word_size_list])
        self.word_size_combobox.currentIndexChanged.connect(self.on_combobox_change_word_size)

    def program_combobox_init(self):
        self.program_combobox.addItems(configs.choice_list)
        self.program_combobox.currentIndexChanged.connect(self.on_combobox_change_layout)

    def on_combobox_change_word_size(self):
        print('on call')
        self.word_size = int(self.word_size_combobox.currentText())
        self.on_combobox_change_type()

    def on_combobox_change_type(self):
        length = self.word_size
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QComboBox):
                line = self.grid_layout.itemAt(i+1).widget()
                new_validator = input_validator(length, widget.currentText())
                if not validator_equal_to(new_validator, line.validator()):
                    line.setValidator(new_validator)
                    line.setText('0')

    def on_combobox_change_layout(self):
        program_name = self.program_combobox.currentText()
        self.text_browser.clear()
        program = getattr(configs.programs, program_name)
        self.current_program = program
        self.description.setText(program.description)

        for i in range(self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().deleteLater()

        for line_number, parameter in enumerate(program.param):
            self.grid_layout.addWidget(QLabel(parameter.name + ':', self), line_number, 0, 1, 1)
            combobox = QComboBox(self)
            line_edit = QLineEdit(self)
            self.grid_layout.addWidget(combobox, line_number, 1, 1, 1)
            self.grid_layout.addWidget(line_edit, line_number, 2, 1, 1)
            combobox.currentIndexChanged.connect(self.on_combobox_change_type)
            combobox.addItems(configs.input_types)
            combobox.setCurrentIndex(parameter.type)

        self.word_size_combobox.currentIndexChanged.disconnect(self.on_combobox_change_word_size)
        self.word_size_combobox.clear()
        self.word_size_combobox.addItems([str(i) for i in configs.word_size_list])
        if hasattr(self.current_program, 'except_word_size'):
            for ws in self.current_program.except_word_size:
                word_size_list = configs.word_size_list
                self.word_size_combobox.removeItem(word_size_list.index(ws))
        self.word_size_combobox.currentIndexChanged.connect(self.on_combobox_change_word_size)

    def compute_func(self):
        input_list = []
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                input_type = self.grid_layout.itemAt(i-1).widget().currentText()
                output_type = configs.input_types[self.current_program.param[i//3].type]
                input_list.append(tools.conversion(input_type, widget.text(), output_type))

        result = tools.compute(self.current_program, self.word_size, configs.binary_file, *input_list)
        self.set_result_func(result)

    def set_result_func(self, result):
        self.text_browser.setText(result)


if __name__ == '__main__':
    configs = configs()
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
