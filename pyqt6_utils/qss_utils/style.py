from __future__ import annotations
from typing import AnyStr
from PyQt6.QtCore import QObject, QPoint, QRect
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
                    f'{r}{unit} {b}{unit}')
        case QPoint():
            return f'{obj.x()}{unit} {obj.y()}{unit}'
    return obj


class Style:
    split_char = '->'
    bind_data = {
        '_obj': 'object_name',
    }

    def __init__(self, qwidget: QWidget = None,
                 init_style: Style | dict = None,
                 object_name: str = 'QWidget') -> None:

        self.set_qwidget(qwidget)

        if isinstance(init_style, Style):
            init_style = init_style.to_dict()
        elif init_style is None:
            init_style = {self.object_name(): dict()}

        self.__style__: dict[str, dict] = init_style.copy()
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

    def __setitem__(self, selector: str, value: str):
        keys = self.__selector_to_keys(selector)

        match keys:
            case [selector, property]:
                p_sel = keys[0].split(':')
                match p_sel:
                    case [obj, pseudo]:
                        self.add_property(property, value, pseudo_class=pseudo)
                    case [obj]:
                        print(obj, property, value)
                        self.add_property(property, value)
            case _:
                raise AttributeError(
                    'Adding an empty pseudo-class '
                    'is only available through the method: '
                    '<Style.add_pseudo_class>'
                )

    def __repr__(self) -> str:
        qss = ''
        for selector, style in self.__style__.items():
            qss += f'\n#{selector} ' + '{'
            for property, value in style.items():
                qss += f'\n    {property}: {value};'
            qss += '\n}'
        return qss

    def __set_object_name(self, object_name: str):
        new_style = {}
        for selector, value in self.__style__.items():
            selector = str(selector)
            new_selector = selector.replace(selector, object_name)
            new_style[new_selector] = value
        self.__style__ = new_style
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

    def add_property(self, property: str, value: str,
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
        self.update_qwidget_qss()

    def remove(self, selector: str) -> str | tuple:
        """ Remove pseudo-class or property """
        if not selector:
            print('\n[Warning]: When removing a pseudo-class, '
                  'you need to explicitly specify the selector on it\n')
            return None

        keys = self.__selector_to_keys(selector)
        match keys:
            case [pseudo]:
                res = self.__style__.pop(pseudo)
            case [pseudo, property]:
                res = self.__style__[pseudo].pop(property)
            case _:
                res = ()
        self.update_qwidget_qss()
        return res

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

    def set_qwidget(self, qwidget: QWidget):
        if isinstance(qwidget, QWidget):
            self.__qwidget = qwidget
            self.__object_name = qwidget.objectName()
            qwidget.objectNameChanged.connect(self.__set_object_name)
        elif qwidget is None:
            try:
                self.__qwidget.objectNameChanged.disconnect(
                    self.__set_object_name)
            except AttributeError:
                pass
            self.__qwidget = None
            self.__object_name = 'QWidget'
        else:
            raise TypeError(f'{qwidget} not is <QWidget>')

    def set_object_name(self, object_name: str):
        self.__qwidget.setObjectName(object_name)

    def to_dict(self) -> dict:
        """ `Return` copy of style dict """
        return self.__style__.copy()

    def qss(self) -> str:
        """ `Return` styleSheet """
        return self.__repr__()

    def object_name(self) -> str:
        """ Возвращает `QWidget.objectName`
            зарегистрированный в Style """
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

    def qwidget(self) -> QWidget:
        return self.__qwidget

    def update_qwidget_qss(self):
        if self.qwidget():
            self.qwidget().setStyleSheet(self.qss())
