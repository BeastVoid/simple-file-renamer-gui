from pathlib import Path
from os import listdir, rename as file_rename
from os.path import (
    isfile,
    normpath,
    join as path_join,
    splitext as os_splitext
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QRadioButton,
    QLabel,
    QProgressBar
)
from PyQt6.QtGui import QFont

ALIGN_CENTER_TOP = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Base attributes
        self.files_to_rename = 0
        self.str_folder_path = ""

        # Directory selection
        path_label = QLabel("Directory")
        path_label.setAlignment(ALIGN_CENTER_TOP)
        file_explore_widget = QWidget()
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        button_open_file_explorer = QPushButton(
            "Select directory",
            file_explore_widget
        )
        button_open_file_explorer.clicked.connect(self._open_file_explorer)

        # Directory reading order
        order_group_widget = QWidget()
        order_group_layout = QHBoxLayout()
        self.order_a_z = QRadioButton("A-Z", order_group_widget)
        self.order_z_a = QRadioButton("Z-A", order_group_widget)
        self.order_a_z.setChecked(True)
        order_group_layout.addWidget(self.order_a_z)
        order_group_layout.addWidget(self.order_z_a)
        order_group_widget.setLayout(order_group_layout)

        # File explorer
        box_layout = QVBoxLayout()
        box_layout.addWidget(path_label)
        box_layout.addWidget(self.folder_path)
        box_layout.addWidget(button_open_file_explorer)
        box_layout.addWidget(order_group_widget)
        file_explore_widget.setLayout(box_layout)

        # File name
        filename_widget = QWidget()
        filename_layout = QVBoxLayout()
        filename_label = QLabel("New file name")
        filename_label.setAlignment(ALIGN_CENTER_TOP)
        self.filename = QLineEdit()
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename)
        filename_widget.setLayout(filename_layout)

        # Naming pattern
        name_pattern_widget = QWidget()
        name_pattern_layout = QVBoxLayout()
        name_pattern_label = QLabel("Naming pattern")
        name_pattern_label.setAlignment(ALIGN_CENTER_TOP)
        self.name_pattern = QLineEdit()
        quick_name_pattern_label = QLabel("Quick naming patterns")
        name_pattern_layout.addWidget(name_pattern_label)
        name_pattern_layout.addWidget(self.name_pattern)
        name_pattern_layout.addWidget(quick_name_pattern_label)
        name_pattern_widget.setLayout(name_pattern_layout)

        # Quick naming options
        quick_name_pattern_widget = QWidget()
        quick_name_pattern_layout = QHBoxLayout()
        quick_tv_series_button = QPushButton("TV Series")
        quick_autoincrement_button = QPushButton("Simple autoincrement")
        quick_tutorial = QPushButton("?")  # TODO add functionality
        quick_name_pattern_layout.addWidget(quick_tv_series_button)
        quick_name_pattern_layout.addWidget(quick_autoincrement_button)
        quick_name_pattern_layout.addWidget(quick_tutorial)
        quick_name_pattern_widget.setLayout(quick_name_pattern_layout)

        # Naming
        naming_widget = QWidget()
        naming_layout = QVBoxLayout()
        naming_layout.addWidget(filename_widget)
        # naming_layout.addWidget(name_pattern_widget)
        # naming_layout.addWidget(quick_name_pattern_widget)
        naming_widget.setLayout(naming_layout)

        # Window settings
        self.window_widget = QWidget()
        self.window_layout = QVBoxLayout()
        self.rename_files_button = QPushButton("Rename files in the directory")
        self.rename_files_button.setFixedHeight(50)
        self.rename_files_button.clicked.connect(self._rename_files)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        status_font = QFont()
        status_font.setItalic(True)
        status_label = QLabel("Awaiting settings...")
        status_label.setAlignment(ALIGN_CENTER_TOP)
        status_label.setFont(status_font)
        self.window_layout.addWidget(file_explore_widget)
        self.window_layout.addWidget(naming_widget)
        self.window_layout.addWidget(self.rename_files_button)
        self.window_layout.addWidget(status_label)
        self.window_layout.addWidget(self.progress_bar)
        self.window_widget.setLayout(self.window_layout)
        self.setCentralWidget(self.window_widget)
        self.setWindowTitle("simple-tvshow-renamer")
        self.setFixedSize(self.size())

    def _open_file_explorer(self):
        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if self.file_dialog.exec():
            directory = self.file_dialog.selectedFiles()[0]
            if directory:
                self.str_folder_path = str(Path(directory))
                self.folder_path.setText(self.str_folder_path)

    def _rename_files(self):
        files_in_directory = []
        target_path = normpath(self.str_folder_path)
        files_list = listdir(target_path)
        print(files_list)
        for f in files_list:
            if isfile(path_join(target_path, f)):
                files_in_directory.append(f)
        files_to_rename = len(files_in_directory)
        self.progress_bar.setMaximum(files_to_rename)
        files_in_directory = sorted(files_in_directory)
        if self.order_z_a.isChecked():
            files_in_directory = sorted(files_in_directory, reverse=True)
        print(files_to_rename)
        self.rename_files_button.setDisabled(True)
        self.progress_bar.setValue(0)
        autonum = 1
        for file in files_in_directory:
            original_file = path_join(target_path, file)
            print(original_file)
            file_extension = os_splitext(original_file)[1]
            print(file_extension)
            new_filename = self.filename.text().rstrip() + " " + str(autonum)
            new_filename += file_extension
            new_file = path_join(
                target_path,
                new_filename
            )
            file_rename(original_file, new_file)
            print(new_file)
            autonum += 1
            self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.rename_files_button.setDisabled(False)
