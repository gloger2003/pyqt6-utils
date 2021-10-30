import os

from PyQt6.QtWidgets import (QApplication, QFileDialog, QLabel, QPushButton,
                             QWidget)


class QFileInputButton(QPushButton):
    def __init__(self, parent: QWidget = None,
                 caption='Open file',
                 direction='c://',
                 filter_caption='Image files',
                 file_extensions=('jpg', 'png', 'gif')):
        super().__init__(parent=parent)

        self.caption = caption
        self.direction = direction
        self.filter_caption = filter_caption
        self.file_extensions = file_extensions
        self.__filename: str = None
        self.__basename: str = None

        self.clicked.connect(self.load_filename)

    def get_filter_str(self) -> str:
        """ Возвращает фильтр для файлов """
        return (f'{self.filter_caption} (' +
                ' '.join([f'*.{k}' for k in self.file_extensions]) + ')')

    def set_filename(self, filename: str):
        self.__filename = filename
        self.__basename = os.path.basename(filename)
        self.setText(self.__basename)

    def load_filename(self) -> tuple[str, str]:
        """ Вызывает диалогое окно """
        filename = QFileDialog.getOpenFileName(
            self, self.caption, self.direction, self.get_filter_str())[0]
        self.set_filename(filename)
        return filename

    def clear_file_data(self):
        self.__filename = self.__basename = None
        self.setText('')

    def filename(self) -> str:
        return self.__filename

    def basename(self) -> str:
        return self.__basename
