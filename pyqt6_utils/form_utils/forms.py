from __future__ import annotations

from typing import Callable

from PyQt6.QtWidgets import (QDoubleSpinBox, QLineEdit,
                             QSpinBox, QTextEdit, QWidget)

from .custom_qwidgets import QFileInputButton
from .form import Form, FormManager, FormValueType


class QLineEditForm(Form):
    """ Форма типа `QLineEdit` """

    def __init__(self, *,
                 form_name: str,
                 parent: QWidget = None,
                 default_value='',
                 converter: Callable = str,
                 form_manager: FormManager = None) -> None:
        super().__init__(form_name, default_value=default_value,
                         converter=converter, form_manager=form_manager)
        self._qwidget = QLineEdit(parent)
        self._qwidget.setObjectName('QLineEditForm')

    def get_value(self):
        return self._converter(self._qwidget.text())

    def set_value(self, value: FormValueType):
        try:
            self._qwidget.setText(str(value))
        except Exception:
            self._qwidget.setText(str(self._default_value)
                                  if self._default_value
                                  else '')

    def restore_value(self):
        self._qwidget.setText(self._default_value)

    def clear_value(self):
        self._qwidget.clear()


class QIntSpinBoxForm(Form):
    """ Форма типа `QIntSpinBox` """

    def __init__(self, *,
                 form_name: str,
                 parent: QWidget = None,
                 default_value=0,
                 min_value: int = 0,
                 max_value: int = 100,
                 converter: Callable = str,
                 form_manager: FormManager = None) -> None:
        super().__init__(form_name, default_value=default_value,
                         converter=converter, form_manager=form_manager)

        self.__default_value_converter = int

        self._qwidget = QSpinBox(parent)
        self._qwidget.setObjectName('QIntSpinBoxForm')
        self._qwidget.setMinimum(min_value)
        self._qwidget.setMaximum(max_value)

    def __set_value_range(self, value: int, func: Callable):
        try:
            func(self.__default_value_converter(value))
        except Exception:
            func(self.__default_value_converter(self._default_value)
                 if self._default_value
                 else 0)

    def get_value(self):
        return self._converter(self._qwidget.value())

    def min_value(self) -> int:
        """ Возвращает минимальное значение формы """
        return self._qwidget.minimum()

    def max_value(self) -> int:
        """ Возвращает максимальное int-значение формы """
        return self._qwidget.maximum()

    def set_min_value(self, value: FormValueType):
        """ Устанавливает минимальное значение формы """
        self.__set_value_range(value, self._qwidget.setMinimum)

    def set_min_value(self, value: FormValueType):
        """ Устанавливает максимальное значение формы """
        self.__set_value_range(value, self._qwidget.setMaximum)

    def restore_value(self):
        self._qwidget.setValue(self._default_value)

    def clear_value(self):
        self._qwidget.clear()

    def set_value(self, value: FormValueType):
        try:
            self._qwidget.setValue(self.__default_value_converter(value))
        except Exception:
            self._qwidget.setValue(
                self.__default_value_converter(self._default_value)
                if self._default_value else 0
            )


class QFloatSpinBoxForm(Form):
    """ Форма типа `QIntSpinBox` """

    def __init__(self, *,
                 form_name: str,
                 parent: QWidget = None,
                 default_value=0,
                 min_value: int = 0,
                 max_value: int = 100,
                 converter: Callable = str,
                 form_manager: FormManager = None) -> None:
        super().__init__(form_name, default_value=default_value,
                         converter=converter, form_manager=form_manager)

        self.__default_value_converter = float

        self._qwidget = QDoubleSpinBox(parent)
        self._qwidget.setObjectName('QFloatSpinBoxForm')
        self._qwidget.setMinimum(min_value)
        self._qwidget.setMaximum(max_value)

    def __set_value_range(self, value: float, func: Callable):
        try:
            func(self.__default_value_converter(value))
        except Exception:
            func(self.__default_value_converter(self._default_value)
                 if self._default_value
                 else 0)

    def get_value(self):
        return self._converter(self._qwidget.value())

    def min_value(self) -> float:
        """ Возвращает минимальное значение формы """
        return self._qwidget.minimum()

    def max_value(self) -> float:
        """ Возвращает максимальное int-значение формы """
        return self._qwidget.maximum()

    def set_min_value(self, value: FormValueType):
        """ Устанавливает минимальное значение формы """
        self.__set_value_range(value, self._qwidget.setMinimum)

    def set_min_value(self, value: FormValueType):
        """ Устанавливает максимальное значение формы """
        self.__set_value_range(value, self._qwidget.setMaximum)

    def restore_value(self):
        self._qwidget.setValue(self._default_value)

    def clear_value(self):
        self._qwidget.clear()

    def set_value(self, value: FormValueType):
        try:
            self._qwidget.setValue(self.__default_value_converter(value))
        except Exception:
            self._qwidget.setValue(
                self.__default_value_converter(self._default_value)
                if self._default_value else 0.0
            )


class QTextEditForm(Form):
    """ Форма типа `QLineEdit` """

    def __init__(self, *,
                 form_name: str,
                 parent: QWidget = None,
                 default_value='',
                 converter: Callable = str,
                 form_manager: FormManager = None) -> None:
        super().__init__(form_name, default_value=default_value,
                         converter=converter, form_manager=form_manager)
        self._qwidget = QTextEdit(parent)
        self._qwidget.setObjectName('QTextEditForm')

        self.__default_converter = str

    def get_value(self):
        return self._converter(self._qwidget.toPlainText())

    def set_value(self, value: FormValueType):
        try:
            self._qwidget.setPlainText(self.__default_converter(value))
        except Exception:
            self._qwidget.setPlainText(
                self.__default_converter(self._default_value)
                if self._default_value else ''
            )

    def restore_value(self):
        self._qwidget.setText(self._default_value)

    def clear_value(self):
        self._qwidget.clear()


class QFileInputButtonForm(Form):
    """ Форма типа `QLineEdit` """

    def __init__(self, *,
                 form_name: str,
                 parent: QWidget = None,
                 default_value='Файл не выбран',
                 converter: Callable = str,
                 form_manager: FormManager = None) -> None:
        super().__init__(form_name, default_value=default_value,
                         converter=converter, form_manager=form_manager)
        self._qwidget: QFileInputButton = QFileInputButton(parent)
        self._qwidget.setObjectName('QFileInputButton')

    def get_value(self):
        return self._converter(self._qwidget.filename())

    def set_value(self, value: str):
        try:
            self._qwidget.set_filename(value)
        except Exception:
            self._qwidget.setText(
                str(self._default_value)
                if self._default_value else ''
            )

    def restore_value(self):
        self._qwidget.clear_filename()
        self._qwidget.setText(self._default_value)

    def clear_value(self):
        self._qwidget.clear_file_data()
