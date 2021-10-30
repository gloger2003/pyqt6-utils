from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from pyqt6_utils.form_utils.custom_qwidgets import QFileInputButton
from pyqt6_utils.form_utils.form import Form, FormManager
from pyqt6_utils.form_utils.forms import (QFileInputButtonForm,
                                          QIntSpinBoxForm, QLineEditForm)


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(640, 480)

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.le_form = QLineEditForm(form_name='line', parent=self.central)
        self.le_form.set_value('line')

        self.file_btn = QFileInputButtonForm(
            form_name='file', parent=self.central
        )


if __name__ == '__main__':
    app = QApplication([])

    window = Window()
    window.show()

    fm = FormManager()
    fm.append_form(window.file_btn)

    print(window.file_btn.qwidget())

    fm.execute_qwidget_method(
        form_name='file',
        method_name='setText',
        method_args=('Сработал')
    )

    app.exec()
