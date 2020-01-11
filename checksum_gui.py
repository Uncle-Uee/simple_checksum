"""
Created By : Ubaidullah Effendi-Emjedi
LinkedIn :
Icon By : https://www.flaticon.com/authors/freepik
"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QAction, qApp, QFileDialog

from checksum import *
from pyqt_creator import *


class checksum_window(QMainWindow):
    """
    Checksum Window Class.
    """

    """ ORIENTATION """
    X_POSITION = 200
    Y_POSITION = 200

    WIDTH = 640
    HEIGHT = 480

    """ TITLE """
    TITLE = "Simple Checksum"

    """ JSON FILE REFERENCE """
    json_file = ""

    """ HASH FUNCTION """
    hash_type = hashlib.blake2b()

    """ COMMON FILE SIZE RANGES """
    FILE_SIZES = {"32mb": 32.0, "64mb": 64.0, "128mb": 128.0, "256mb": 256.0, "512mb": 512.0, "1024mb": 1024.0,
                  "2048mb": 2048.0, "4096mb": 4096.0}

    custom_file_size = 0

    checksum_string = ""

    checksum_data = []

    """ CONSTRUCTOR """

    def __init__(self):
        super(checksum_window, self).__init__()
        self.main_window_setup()
        self.menu_bar()
        self.main_window_layout_setup()
        self.ui()

    """ FUNCTIONS """

    def main_window_setup(self):
        """
        Adjust Main Window Parameters such as Geometry and Title etc
        :return:
        """
        self.setGeometry(self.X_POSITION, self.Y_POSITION, self.WIDTH, self.HEIGHT)
        self.setWindowTitle(self.TITLE)
        self.setWindowIcon(QIcon("checksum.ico"))

    def menu_bar(self):
        """
        Create a Menu Bar with Tabs and Actions
        :return:
        """

        # Create MenuBar
        self.bar = self.menuBar()

        # Create Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Create Root Menus
        file_menu = self.bar.addMenu("File")

        # Create Actions for Menus
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open a Checksum File")

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save Calculated Checksum File")

        quit_action = QAction('Quit', self)
        quit_action.setShortcut("Ctrl+Q")

        # Add Actions
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(quit_action)

        # Events
        open_action.triggered.connect(self.open_file_dialog)
        save_action.triggered.connect(lambda: self.save_file_dialog())
        quit_action.triggered.connect(lambda: (qApp.quit(), print("Close Application!")))

    def main_window_layout_setup(self):
        """
        Main Window Layout Setup
        :return:
        """
        # Create a Central Widget.
        self.central_widget = create_widget()
        self.setCentralWidget(self.central_widget)

        # Create UI Button Group
        self.ui_group = QButtonGroup(self)

        # Create Form Layout.
        self.form_layout = QFormLayout()

    def ui(self):
        """
        Create UI Widgets and Layouts Functions.
        Functions create Widgets and Layouts that are added to the Vertical Layout.
        :return:
        """
        # CUSTOM GUI
        secure_hash_type_hlayout = self.choose_hash_type()
        file_size_hlayout = self.choose_file_sizes_to_ignore()
        self.log_file = self.checksum_log_file()
        self.hash_button = self.calculate_hash_button()

        # Create Vertical Layout
        vertical_layout = QVBoxLayout(self.central_widget)

        # Add Form and Horizontal Layout to Vertical Layout
        vertical_layout.addLayout(self.form_layout)
        vertical_layout.addLayout(secure_hash_type_hlayout)
        vertical_layout.addLayout(file_size_hlayout)

        # Add Widgets to Vertical Layout.
        vertical_layout.addWidget(self.log_file)
        vertical_layout.addWidget(self.hash_button)

        # Set MainWindow Layout to Vertical Layout
        self.setLayout(vertical_layout)

    def choose_hash_type(self):
        """
        Choose a Hashing Algorithm. Each Hashing Algorithm has its own benefits. The most secure to use are Blake2,
        SHA256, SHA512 and SHA3 implementations.
        I omitted SHA224, SHA384, SHA3_224 and SHA3_384 because there are many options already available. They can be added
        if requested or you can add them yourself.
        :return:
        """
        # Create Check Boxes
        self.blake2_checkbox = create_check_box(text = "Blake2",
                                                tooltip = "Use Blake2 Hash Algorithm")
        self.sha256_checkbox = create_check_box(text = "SHA256", tooltip = "Use SHA256 Hash Algorithm.")
        self.sha224_checkbox = create_check_box(text = "SHA224", tooltip = "Use SHA224 Hash Algorithm.")
        self.sha384_checkbox = create_check_box(text = "SHA384", tooltip = "Use SHA384 Hash Algorithm.")
        self.sha512_checkbox = create_check_box(text = "SHA512", tooltip = "Use SHA512 Hash Algorithm.")
        self.sha3_256_checkbox = create_check_box(text = "SHA3_256",
                                                  tooltip = "Use SHA3_256 Hash Algorithm.")
        self.sha3_224_checkbox = create_check_box(text = "SHA3_224",
                                                  tooltip = "Use SHA3_224 Hash Algorithm.")
        self.sha3_384_checkbox = create_check_box(text = "SHA3_384",
                                                  tooltip = "Use SHA3_384 Hash Algorithm.")
        self.sha3_512_checkbox = create_check_box(text = "SHA3_512",
                                                  tooltip = "Use SHA3_512 Hash Algorithm.")

        self.blake2_checkbox.setChecked(True)

        # Set Events for State Changed
        self.blake2_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.blake2_checkbox.isChecked(), hashlib.blake2b))
        self.sha3_224_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha3_224_checkbox.isChecked(), hashlib.sha3_224))
        self.sha3_256_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha3_256_checkbox.isChecked(), hashlib.sha3_256))
        self.sha3_384_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha3_384_checkbox.isChecked(), hashlib.sha3_384))
        self.sha3_512_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha3_512_checkbox.isChecked(), hashlib.sha3_512))
        self.sha224_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha224_checkbox.isChecked(), hashlib.sha224))
        self.sha256_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha256_checkbox.isChecked(), hashlib.sha256))
        self.sha384_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha384_checkbox.isChecked(), hashlib.sha384))
        self.sha512_checkbox.stateChanged.connect(
            lambda: self.change_hash_type(self.sha512_checkbox.isChecked(), hashlib.sha512))

        # Add Buttons to UI Group
        self.ui_group.addButton(self.blake2_checkbox)
        self.ui_group.addButton(self.sha3_224_checkbox)
        self.ui_group.addButton(self.sha3_256_checkbox)
        self.ui_group.addButton(self.sha3_384_checkbox)
        self.ui_group.addButton(self.sha3_512_checkbox)
        self.ui_group.addButton(self.sha224_checkbox)
        self.ui_group.addButton(self.sha256_checkbox)
        self.ui_group.addButton(self.sha384_checkbox)
        self.ui_group.addButton(self.sha512_checkbox)

        # Create Horizontal Layout 1.
        horizontal_layout1 = create_horizontal_layout(self.blake2_checkbox, self.sha3_224_checkbox,
                                                      self.sha3_256_checkbox, self.sha3_384_checkbox,
                                                      self.sha3_512_checkbox, self.sha224_checkbox,
                                                      self.sha256_checkbox,
                                                      self.sha384_checkbox, self.sha512_checkbox)

        horizontal_layout1.addStretch()

        # Add Horizontal Layout to Form Layout.
        self.form_layout.addRow("Secure Hash Types:", horizontal_layout1)

        return horizontal_layout1

    def choose_file_sizes_to_ignore(self):
        """
        Choose a file Size to Ignore.
        Any Files greater than the selected or custom input file size in Megabytes will be ignore.
        :return: Horizontal Layout.
        """
        # Create Check Box
        self.skip_file_checkbox = create_check_box(
            tooltip = "Skip Files that are bigger than the chosen or given size in megabytes.")

        # Create Combo Box
        self.combo_box = QComboBox()
        self.combo_box.addItems(
            ["32mb", "64mb", "128mb", "256mb", "512mb", "1024mb", "2048mb", "4096mb", "Custom Size(MB)"])
        self.combo_box.hide()

        # Create Line Edit
        self.file_size_line_edit = create_line_edit(hint = "Size in MB, i.e 128")
        self.file_size_line_edit.hide()

        # Set Skip File Checkbox Action
        self.skip_file_checkbox.stateChanged.connect(
            lambda: self.choose_file_size_active(self.skip_file_checkbox.isChecked()))

        # Activate Line Edit
        self.combo_box.activated[str].connect(
            lambda: self.set_file_size_line_edit_active(self.combo_box.currentText()))

        # Create Horizontal Layout.
        horizontal_layout = create_horizontal_layout(self.skip_file_checkbox, self.combo_box,
                                                     self.file_size_line_edit)
        horizontal_layout.addStretch()

        # Add Horizontal Layout to Form Layout.
        self.form_layout.addRow("Skip Files", horizontal_layout)

        return horizontal_layout

    def checksum_log_file(self):
        """
        Create Checksum Log File
        :return:
        """
        # Create Line Edit Widget
        log_file = create_text_edit()

        # Set to ReadOnly True
        log_file.setReadOnly(True)

        return log_file

    def calculate_hash_button(self):
        hash_button = create_button(text = "Calculate Hash")
        hash_button.clicked.connect(lambda: self.calculate_checksum_data())
        return hash_button

    def compare_new_checksum_with_checksum_file(self):
        pass

    def calculate_checksum_data(self):
        paths = get_path_to_all_files(ignore_files = ["checksum.json", os.path.basename(__file__)])

        print(self.hash_type)

        if self.skip_file_checkbox.isChecked():

            # Get Custom File Size
            self.custom_file_size = self.get_file_size(self.combo_box.currentText())
            if self.blake2_checkbox.isChecked():

                self.checksum_data = [(path, size_cap_checksum_blake2(path,
                                                                      size_cap_in_mb = self.custom_file_size))
                                      for path in paths]
            else:
                self.checksum_data = [
                    (
                        path,
                        size_cap_checksum(path, hash_type = self.hash_type(), size_cap_in_mb = self.custom_file_size))
                    for path in paths]
        else:
            if self.blake2_checkbox.isChecked():
                self.checksum_data = [(path, checksum_blake2(path)) for path in paths]
            else:
                self.checksum_data = [(path, checksum(path, hash_type = self.hash_type())) for path in paths]

        self.set_log_file_text(stringify_checksum_data_array(self.checksum_data))

    def open_file_dialog(self):
        """
        Select and Open a Checksum File.
        :return:
        """
        # Create Dialog Options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Save Path
        path, _ = QFileDialog.getOpenFileName(self, "Open Checksum File", "",
                                              "All Files (*);;Json (*.json)", options = options)

        # If the Path is not Empty String
        if path:
            # Open the File
            self.json_file = open(path, mode = "r")
            # Store Checksum data
            self.checksum_string = self.json_file.read()
            self.checksum_data = checksum_data_dict_to_array(json.loads(self.checksum_string))
            self.set_log_file_text(text = stringify_checksum_data_array(self.checksum_data))

            print(self.checksum_data)

    def save_file_dialog(self):
        """
        Save Checksum Data.
        :return:
        """
        # Create QFile Dialog Options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Store the Path
        path, _ = QFileDialog.getSaveFileName(self, "Save Checksum Data", "",
                                              "All Files (*);;Json Files (*.json)", options = options)

        # Save the Checksum Data if log_file is not an Empty String.
        if path and self.log_file != "":
            write_checksum_to_json(self.checksum_data, path = path)
        else:
            print("No Checksum Data to Save")

    def set_log_file_text(self, text = ""):
        """
        Set Log File Text
        :param text: Checksum Data as String Format
        :return:
        """
        self.log_file.setFontPointSize(10)
        self.log_file.setText(text)

    def change_hash_type(self, is_checked = False, hash_type = hashlib.blake2b):
        """
        Change Hash Algorithm
        :param is_checked: Checkbox is Checked Value
        :param hash_type: Hash Algorithm to Use.
        :return:
        """
        if is_checked:
            self.hash_type = hash_type

    def choose_file_size_active(self, is_checked = False):
        """
        Activate File Size Combo Box if Skip File Size is Checked.
        :param is_checked: Checkbox is Checked Value.
        :return:
        """
        if is_checked:
            self.combo_box.show()
        else:
            self.file_size_line_edit.hide()
            self.reset_combo_box(0)

    def get_file_size(self, current_value = ""):
        """
        Get the Correct File Size from FILE_SIZE Dictionary or User Input
        :param current_value:
        :return:
        """
        try:
            if current_value != "Custom Size(MB)":
                return self.FILE_SIZES[current_value]
            else:
                return int(self.file_size_line_edit)
        except ValueError | ArithmeticError:
            print(f"{ValueError} or {ArithmeticError}")

    def set_file_size_line_edit_active(self, text = ""):
        """
        Enter Custom File Size
        :param text:
        :return:
        """
        if text == "Custom Size(MB)":
            self.file_size_line_edit.show()
        else:
            self.file_size_line_edit.hide()

    def reset_combo_box(self, index = -1):
        """
        Reset Combo Box Options
        :param
        index: Option Index
        :return:
        """
        self.combo_box.hide()
        self.combo_box.setCurrentIndex(index)


def window():
    application = QApplication(sys.argv)
    win = checksum_window()
    win.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    window()
