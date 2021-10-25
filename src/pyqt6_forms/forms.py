from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeAlias

from PyQt6.QtWidgets import QLineEdit, QSpinBox, QWidget


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
        self.qwidget = QLineEdit(parent)
        self.qwidget.setObjectName('QLineEditForm')

    def get_value(self):
        return self._converter(self.qwidget.text())

    def set_value(self, value: FormValueType):
        try:
            self.qwidget.setText(str(value))
        except Exception:
            self.qwidget.setText(str(self._default_value)
                                 if self._default_value
                                 else '')

    def restore_value(self):
        self.qwidget.setText(self._default_value)

    def clear_value(self):
        self.qwidget.clear()


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

        self.qwidget = QSpinBox(parent)
        self.qwidget.setObjectName('QLineEditForm')
        self.qwidget.setMinimum(min_value)
        self.qwidget.setMaximum(max_value)

    def __set_value_range(self, value: int, func: Callable):
        try:
            func(self.__default_value_converter(value))
        except Exception:
            func(self.__default_value_converter(self._default_value)
                 if self._default_value
                 else 0)

    def get_value(self):
        return self._converter(self.qwidget.value())

    def min_value(self) -> int:
        """ Возвращает минимальное значение формы """
        return self.qwidget.minimum()

    def max_value(self) -> int:
        """ Возвращает максимальное int-значение формы """
        return self.qwidget.maximum()

    def set_min_value(self, value: FormValueType):
        """ Устанавливает минимальное значение формы """
        self.__set_value_range(value, self.qwidget.setMinimum)

    def set_min_value(self, value: FormValueType):
        """ Устанавливает максимальное значение формы """
        self.__set_value_range(value, self.qwidget.setMaximum)

    def restore_value(self):
        self.qwidget.setValue(self._default_value)

    def clear_value(self):
        self.qwidget.clear()

    def set_value(self, value: FormValueType):
        try:
            self.qwidget.setValue(self.__default_value_converter(value))
        except Exception:
            self.qwidget.setValue(
                self.__default_value_converter(self._default_value)
                if self._default_value else 0
            )
