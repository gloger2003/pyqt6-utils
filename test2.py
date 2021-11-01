from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from pyqt6_utils.qss_utils.style import Style

style = Style()

style.add_pseudo_class('!hover')
style.add_property('padding', (0, 0, 0, 0), '!hover', 'px')
style.add_property('margin', (0, 0), '!hover', 'px')

style.add_property('color', 'blue')
style.add_property('background-color', 'white')

style['_obj->color'] = 'ggggg'

style.add_pseudo_class('hover')
style.add_property('margin', '0px', 'hover')
style.add_property('color', QColor(10, 10, 10), 'hover')

style['hover'] = ''

# print(style[':!hover'])
# print(style[':!hover->margin'])
# print(style[':hover']['color'])
# print(style.get('').get('background-color'))


# print(style)


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(640, 480)

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.btn = QPushButton(self.central)
        self.btn.setObjectName('b')

        self.btn_style = Style(self.btn, {'b': {'margin': '11px'}})
        self.btn.setObjectName('btn')
        self.btn_style.add_property('background-color', QColor(0, 0, 0))
        self.btn_style.add_pseudo_class('hover')
        self.btn_style.add_property('background-color',
                                    QColor(50, 50, 50), 'hover')
        self.btn_style.add_property('border-radius', 10, 'hover')
        self.btn_style.add_property('width', 200, unit='px')
        self.btn_style.add_property('height', 40, unit='px')

        self.btn_style.remove(':hover->border-radius')

        self.btn_style[':hover->border-radius'] = '10px'

        print(self.btn.styleSheet())


if __name__ == '__main__':
    app = QApplication([])

    window = Window()
    window.show()

    app.exec()
