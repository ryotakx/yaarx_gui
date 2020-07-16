import sys
import tools
from tools import validator_equal_to, input_validator, configs
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QTextBrowser, QDesktopWidget
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
        self.center()

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
        # self.word_size_combobox.setCurrentIndex(2)
        self.word_size_combobox.currentIndexChanged.connect(self.on_combobox_change_word_size)

    def program_combobox_init(self):
        self.program_combobox.addItems(configs.choice_list)
        self.program_combobox.currentIndexChanged.connect(self.on_combobox_change_layout)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def on_combobox_change_word_size(self):
        self.word_size = int(self.word_size_combobox.currentText())
        self.on_combobox_change_type()

    def on_combobox_change_type(self):
        # length = self.word_size // 4
        length = 8
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QComboBox):
                line = self.grid_layout.itemAt(i+1).widget()
                line.setText('0')
                new_validator = input_validator(length, widget.currentText())
                if not validator_equal_to(new_validator, line.validator()):
                    # print('update validator')
                    line.setValidator(new_validator)

    def on_line_edit_change_input(self, text):
        max_word_size = 0
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QComboBox):
                line = self.grid_layout.itemAt(i + 1).widget()
                # name = self.grid_layout.itemAt(i - 1).widget()
                # print(name.text())
                # print(tools.compute_word_size(widget.currentText(), line.text()))
                max_word_size = max(max_word_size, tools.compute_word_size(widget.currentText(), line.text()))
        # print(max_word_size)
        # print('word: %s' % self.word_size)
        if max_word_size * 4 > self.word_size:
            i = self.word_size_combobox.currentIndex()
            self.word_size_combobox.currentIndexChanged.disconnect(self.on_combobox_change_word_size)
            self.word_size_combobox.setCurrentIndex(min(i+1, 3))
            self.word_size = int(self.word_size_combobox.currentText())
            self.word_size_combobox.currentIndexChanged.connect(self.on_combobox_change_word_size)

    def on_combobox_change_layout(self):
        program_name = self.program_combobox.currentText()
        self.text_browser.clear()
        program = getattr(configs.programs, program_name)
        self.current_program = program
        self.description.setText(program.description)

        self.word_size_combobox.currentIndexChanged.disconnect(self.on_combobox_change_word_size)
        self.word_size_combobox.clear()
        self.word_size_combobox.addItems([str(i) for i in configs.word_size_list])
        # self.word_size_combobox.setCurrentIndex(2)
        if hasattr(self.current_program, 'except_word_size'):
            for ws in self.current_program.except_word_size:
                word_size_list = configs.word_size_list
                self.word_size_combobox.removeItem(word_size_list.index(ws))
        self.word_size_combobox.currentIndexChanged.connect(self.on_combobox_change_word_size)
        self.word_size = int(self.word_size_combobox.currentText())
        # print('change_layout: %s' % self.word_size)

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
            line_edit.textEdited.connect(self.on_line_edit_change_input)

    def compute_func(self):
        self.set_result_func('Computing...')
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
