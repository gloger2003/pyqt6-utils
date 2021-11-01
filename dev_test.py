from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor
from pyqt6_utils.qss_utils.style import to_str


class A:
    pass


class B(A):
    def __init__(self) -> None:
        super().__init__()


print(isinstance(B(), object))
