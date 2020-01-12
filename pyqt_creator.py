from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


def create_widget():
    widget = QWidget()
    return widget


def create_vertical_layout(*layout_fields):
    vertical_box = QVBoxLayout()
    for field in layout_fields:
        vertical_box.addWidget(field)

    return vertical_box


def create_horizontal_layout(*layout_fields):
    horizontal_box = QHBoxLayout()
    for field in layout_fields:
        horizontal_box.addWidget(field)

    return horizontal_box


def create_label(orientation = (0, 0, 0, 0), text = ""):
    """
    Create a Label.
    :param orientation: Orientation of the label: X,Y Position and Width and Height
    :param text: Label Text
    :return: QTWidget Label
    """
    label = QLabel(text)
    label.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
    return label


def create_label(text = ""):
    """
    Create a Label.
    :param text: Label Text
    :return: QTWidget Label
    """
    label = QLabel(text)
    return label


def create_button(orientation = (0, 0, 0, 0), text = "button"):
    """
    Create a Button.
    :param orientation: Orientation of the button: X,Y Position and Width and Height
    :param text: Button Text
    :return: QTWidget Push Button
    """
    button = QPushButton(text)
    button.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
    return button


def create_button(text = "button"):
    """
    Create a Button.
    :param text: Button Text
    :return: QTWidget Push Button
    """
    button = QPushButton(text)
    return button


def create_check_box(orientation = (0, 0, 0, 0), text = ""):
    """
    Create a Check Box Option.
    :param orientation: Placement of the Check Box.
    :param text: Check Box Text.
    :return:
    """
    check_box = QCheckBox(text)
    check_box.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
    check_box.setText(text)
    check_box.adjustSize()
    return check_box


def create_check_box(text = "", tooltip = ""):
    """
    Create a Check Box Option
    :param text: Check Box Text.
    :param tooltip: Hint about GUI Item
    :return: Check box.
    """
    check_box = QCheckBox(text)
    check_box.setToolTip(tooltip)
    check_box.setText(text)
    check_box.adjustSize()
    return check_box


def create_line_edit(orientation = (0, 0, 0, 0), text = "", hint = ""):
    """
    Create a Text Box Input Field
    :param orientation: Placement of the Text Box Field.
    :param text: Text Box Text
    :param hint: Text Box Hint Text
    :return: QLineEdit
    """
    text_box = QLineEdit(text)
    text_box.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
    text_box.setPlaceholderText(hint)
    return text_box


def create_line_edit(text = "", hint = ""):
    """
    Create a Text Box Input Field
    :param text: Text Box Text
    :param hint: Text Box Hint Text
    :return: QLineEdit
    """
    text_box = QLineEdit(text)
    text_box.setPlaceholderText(hint)
    return text_box


def create_text_edit(text = "", tooltip = ""):
    """
    Create Text Edit Field
    :param text:
    :param tooltip:
    :return: QTextEdit
    """
    text_edit = QTextEdit()
    text_edit.setText(text)
    text_edit.setToolTip(tooltip)
    return text_edit


def create_font(font = "", size = 8):
    """
    Create Font
    :param font: Type of Font to Use.
    :param size: Size of the Font.
    :return: QtGUI Font
    """
    font = QFont(font, pointSize = size)
    return font
