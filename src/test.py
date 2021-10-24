from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from pyqt6_forms.form import Form, FormManager
from pyqt6_forms.forms import QIntSpinBoxForm, QLineEditForm


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1280, 720)

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.le_form = QLineEditForm(form_name='line', parent=self.central)
        self.le_form.set_value('line')


if __name__ == '__main__':
    app = QApplication([])

    window = Window()
    window.show()

    fm = FormManager()
    fm.append_forms([QIntSpinBoxForm(form_name='ffff'),
                     QIntSpinBoxForm(form_name='spin')])
    print(fm)

    app.exec()
