from PyQt6.QtGui import QColor
from pyqt6_utils.qss_utils.style import Style

style = Style()

style.add_pseudo_class('!hover')
style.set_property('padding', (0, 0, 0, 0), '!hover', 'px')
style.set_property('margin', (0, 0), '!hover', 'px')

style.set_property('color', 'blue')
style.set_property('background-color', 'white')

style.add_pseudo_class('hover')
style.set_property('margin', '0px', 'hover')
style.set_property('color', QColor(10, 10, 10), 'hover')


print(style[':!hover'])
print(style[':!hover->margin'])
print(style[':hover']['color'])
print(style.get('').get('background-color'))


print(style.to_dict())
