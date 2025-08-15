import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QFileDialog,
    QMessageBox
)

from utils.image_packer.image_packer import ImagePacker


class ImagePackerUI(QMainWindow):

    LABEL_WIDTH = 100
    BUTTON_WIDTH = 150

    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.setWindowTitle("Image Packer")
        self.setGeometry(100, 100, 800, 200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        horizontal_container = QHBoxLayout()
        label = QLabel("Source Folder")
        label.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        self.edit_source = QLineEdit()
        self.btn_get_source = QPushButton("Get Source Folder")
        self.btn_get_source.setFixedWidth(ImagePackerUI.BUTTON_WIDTH)
        horizontal_container.addWidget(label)
        horizontal_container.addWidget(self.edit_source)
        horizontal_container.addWidget(self.btn_get_source)
        main_layout.addLayout(horizontal_container)

        horizontal_container = QHBoxLayout()
        label = QLabel("Amount of files")
        label.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        self.lbl_image_count = QLabel("0")
        self.lbl_image_count.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        horizontal_container.addWidget(label)
        horizontal_container.addWidget(self.lbl_image_count)
        horizontal_container.addItem(spacer)
        main_layout.addLayout(horizontal_container)

        horizontal_container = QHBoxLayout()
        label = QLabel("Target file")
        label.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        self.edit_target = QLineEdit()
        self.btn_get_target = QPushButton("Set target file")
        self.btn_get_target.setFixedWidth(ImagePackerUI.BUTTON_WIDTH)
        horizontal_container.addWidget(label)
        horizontal_container.addWidget(self.edit_target)
        horizontal_container.addWidget(self.btn_get_target)
        main_layout.addLayout(horizontal_container)

        horizontal_container = QHBoxLayout()
        label = QLabel("Columns")
        label.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        self.edit_cols = QLineEdit()
        self.edit_cols.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        horizontal_container.addWidget(label)
        horizontal_container.addWidget(self.edit_cols)
        horizontal_container.addItem(spacer)
        main_layout.addLayout(horizontal_container)

        horizontal_container = QHBoxLayout()
        label = QLabel("Rows")
        label.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        self.edit_rows = QLineEdit()
        self.edit_rows.setFixedWidth(ImagePackerUI.LABEL_WIDTH)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        horizontal_container.addWidget(label)
        horizontal_container.addWidget(self.edit_rows)
        horizontal_container.addItem(spacer)
        main_layout.addLayout(horizontal_container)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer)

        horizontal_container = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.btn_pack = QPushButton("Pack")
        self.btn_pack.setFixedWidth(ImagePackerUI.BUTTON_WIDTH)
        horizontal_container.addItem(spacer)
        horizontal_container.addWidget(self.btn_pack)
        main_layout.addLayout(horizontal_container)

        self.btn_get_source.clicked.connect(self.btn_get_source_clicked)
        self.btn_get_target.clicked.connect(self.btn_set_target_clicked)
        self.btn_pack.clicked.connect(self.btn_pack_clicked)

    def btn_get_source_clicked(self):
        file_dialog = QFileDialog()
        #file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        clicked_button = file_dialog.exec()
        if clicked_button:
            selected_files = file_dialog.selectedFiles()
            self.edit_source.setText(selected_files[0])
            entries = os.listdir(selected_files[0])
            self.lbl_image_count.setText(str(len(entries)))
            cols, rows = ImagePacker.get_suggested_layout(len(entries))
            self.edit_cols.setText(str(cols))
            self.edit_rows.setText(str(rows))


    def btn_set_target_clicked(self):
        file_dialog = QFileDialog()
        clicked_button = file_dialog.exec()
        if clicked_button:
            selected_files = file_dialog.selectedFiles()
            self.edit_target.setText(selected_files[0])

    def btn_pack_clicked(self):

        image_packer = ImagePacker()
        result = image_packer.pack(self.edit_source.text(), self.edit_target.text(), self.edit_cols.text(), self.edit_rows.text())
        print(result)

        dialog = QMessageBox()
        dialog.setText("Packing completed")
        dialog.setWindowTitle("Please note")
        dialog.setIcon(QMessageBox.Icon.Information)

        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        clicked_button = dialog.exec()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ImagePackerUI()
    window.show()
    sys.exit(app.exec())