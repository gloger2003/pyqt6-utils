from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from src.pyqt6_forms.custom_qwidgets import QFileInputButton
from src.pyqt6_forms.form import Form, FormManager
from src.pyqt6_forms.forms import QIntSpinBoxForm, QLineEditForm


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(640, 480)

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.le_form = QLineEditForm(form_name='line', parent=self.central)
        self.le_form.set_value('line')

        self.file_btn = QFileInputButton(parent=self.central)


if __name__ == '__main__':
    app = QApplication([])

    window = Window()
    window.show()

    fm = FormManager()
    fm.append_forms([QIntSpinBoxForm(form_name='ffff'),
                     QIntSpinBoxForm(form_name='spin')])

    app.exec()
