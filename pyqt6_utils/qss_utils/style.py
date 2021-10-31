from __future__ import annotations
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QColor

from PyQt6.QtWidgets import QWidget
import json


def to_str(obj: QRect | QColor | QPoint, unit: str = 'px') -> str:
    match obj:
        case str() if unit:
            return f'{obj}{unit}'
        case int():
            return f'{obj}{unit}'
        case QColor():
            return obj.name()
        case QRect():
            return (f'{obj.left()}{unit} {obj.top()}{unit} '
                    f'{obj.right()}{unit} {obj.bottom()}{unit}')
        case (x, y) | [x, y]:
            return (f'{x}{unit} {y}{unit}')
        case (l, t, r, b) | [l, t, r, b]:
            return (f'{l}{unit} {t}{unit} '
                    f'{r}{unit} {b}{unit} ')
        case QPoint():
            return f'{obj.x()}{unit} {obj.y()}{unit}'
    return obj


class Style:
    split_char = '->'
    bind_data = {
        '_obj': 'object_name',
    }

    def __init__(self, qwidget: QWidget = None,
                 init_style: Style | dict = {},
                 object_name: str = 'QWidget') -> None:
        if isinstance(init_style, Style):
            init_style = init_style.to_dict()
        elif not isinstance(init_style, dict):
            raise TypeError(f'init_style not is Style or Dict')

        if isinstance(qwidget, QWidget):
            self.__object_name = qwidget.objectName()
            qwidget.objectNameChanged.connect(self.__set_object_name)
        else:
            self.__object_name = object_name

        self.__style__ = init_style
        self.__style__[self.__object_name] = dict()
        self.__qwidget: QWidget = qwidget

    def __getitem__(self, selector: str) -> str | dict:
        try:
            keys = self.__selector_to_keys(selector)
            value = self.__style__
            for key in keys:
                value = value.get(key)
            if isinstance(value, dict):
                value = value.copy()
        except AttributeError:
            value = None
        return value

    def __repr__(self) -> str:
        qss = json.dumps(self.__style__, indent=4)
        qss = qss.replace(',', ';')
        return qss

    def __set_object_name(self, object_name: str):
        for selector, value in self.__style__.items():
            selector = str(selector)
            new_selector = selector.replace(selector, object_name)
            self.__style__[new_selector] = value
            self.__style__.pop(selector)
        self.__object_name = object_name

    def __selector_to_keys(self, selector: str):
        # Проверяем, явно ли указан QWidget
        # если нет, то указываем сами
        obj = selector.split(':')[0]
        if not obj:
            selector = self.object_name() + selector

        # Методом постоянного извлечения получаем конечное значение
        for bind, method_name in __class__.bind_data.items():
            selector = selector.replace(bind, getattr(self, method_name)())

        # Разделяем и убираем пустые строки
        keys = selector.split(__class__.split_char)
        keys = [k.strip(' ') for k in filter(bool, keys)]

        # Если список пуст, то гарантировано возвращаем
        # селектор на QWidget
        if not keys:
            keys = [self.object_name()]
        return keys

    def set_property(self, property: str, value: str,
                     pseudo_class: str = '', unit: str = ''):
        """ Добавляет либо изменяет указанное свойства \n
            `selector` - селектор псевдокласса \n
            `unit` - единица измерения (px) \n
        """
        # Делаем преобразование псевдо-класса в селектор
        if pseudo_class and pseudo_class[0] != ':':
            pseudo_class = f':{pseudo_class}'

        # Гарантированно получаем селектор на текущий QWidget
        selector = self.__selector_to_keys(pseudo_class)[0]

        # Преобразуем и устанавливаем новое свойство
        # указанному селектору
        self.__style__[selector][property] = to_str(value, unit)

    def add_pseudo_class(self, pseudo_class: str) -> str:
        """ Добавляет новый селектор с указанным псевдо-классом \n
            Example:
                `"QWidget:hover"` = `add_pseudo_class('hover')` \n
                `"QWidget:!hover"` = `add_pseudo_class('!hover')`
            Return:
                Преобразованный селектор
        """
        selector = f'{self.object_name()}:{pseudo_class}'
        self.__style__[selector] = dict()
        return selector

    def set_object_name(self, object_name: str):
        self.__qwidget.setObjectName(object_name)

    def to_dict(self) -> dict:
        return self.__style__.copy()

    def qss(self) -> str:
        return self.__repr__()

    def object_name(self) -> str:
        """ Обёртка для `QWidget.objectName()` """
        return self.__object_name

    def clear(self) -> str:
        """ Полностью очищает StyleSheet """
        self.__style__.clear()
        self.__style__[self.object_name()] = dict()
        self.__qwidget.setStyleSheet(
            f'{self.object_name()} ' + '{}'
            f'{self.object_name()}:* ' + '{}'
        )

    def get(self, selector: str) -> str | dict:
        """ Обёртка для `Style[selector]` """
        return self[selector]
