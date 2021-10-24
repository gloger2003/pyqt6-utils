from PyQt6.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1280, 720)


if __name__ == '__main__':
    app = QApplication([])

    window = Window()
    window.show()

    app.exec()
