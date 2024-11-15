import sys
import csv
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QLabel, QTextEdit, QComboBox, QCheckBox, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore, QtGui
from PLC_CommandClass import *

__program__ = 'PLC_Monitor'
kv = kvHostLink('192.168.0.10')

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = __program__
        self.left = 1250
        self.top = 100
        self.width = 768
        self.height = 1024
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # メインウィジェット
        self.main_widget = QWidget(self)
        
        # 縦並びレイアウト
        self.layout = QVBoxLayout(self.main_widget)
        
        # 2つのウィジェットを作成
        self.table_widget1 = CommandLogTable(self, "Command Log")  # Command Logウィジェット（スクロールできるテキストボックス）
        self.table_widget2 = CommandLogTable(self, "Device Status", "Table")  # Device Statusウィジェット（テーブルあり）
        
        # ウィジェットをレイアウトに追加
        self.layout.addWidget(self.table_widget1)
        self.layout.addWidget(self.table_widget2)
        
        # 両方のウィジェットに均等なサイズを割り当て
        self.layout.setStretch(0, 1)  # table_widget1のサイズの伸縮比
        self.layout.setStretch(1, 1)  # table_widget2のサイズの伸縮比
        
        # メインウィジェットを設定
        self.setCentralWidget(self.main_widget)

        self.Initialize_PLC()

        self.show()
    
    def Initialize_PLC(self):
        
        # Sample PLC commands and capture the results
        PLCdata = kv.mode('1')
        self.append_to_log(f"mode('1'): {PLCdata}")
        PLCdata = kv.er()
        self.append_to_log(f"er(): {PLCdata}")
        PLCdata = kv.errclr()
        self.append_to_log(f"errclr(): {PLCdata}")
        PLCdata = kv.unittype()
        self.append_to_log(f"unittype(): {PLCdata}")
        PLCdata = kv.settime()
        self.append_to_log(f"settime(): {PLCdata}")
    
    def append_to_log(self, text):
        # Append the text to the QTextEdit widget in Command Log
        self.table_widget1.text_edit.append(text)
    
class CommandLogTable(QWidget):

    def __init__(self, parent, title, table_name=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.main_window = parent
        
        # タイトルラベルを追加
        self.title_label = QLabel(title, self)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.layout.addWidget(self.title_label)
        
        if table_name:  # table_nameが指定されている場合のみテーブルを作成
            # QTableWidgetを作成
            self.table = QTableWidget()
            self.table.setRowCount(5)       # 行数を設定
            self.table.setColumnCount(8)    # 列数を設定
            self.table.setHorizontalHeaderLabels(["Type", "Num", "Elements", "Status", "Query", "Run", "Enable", "String"])
            
            # 列幅の初期設定
            for col in range(7):
                self.table.setColumnWidth(col, 90)  # すべての列の幅を90pxに設定
            self.table.setColumnWidth(7, 300)

            # 行高さの初期設定
            for row in range(5):
                self.table.setRowHeight(row, 50)  # すべての行の高さを50pxに設定
            
            # CSVからTypeとQueryの列を取得してダウンリストに設定
            self.type_list, self.query_list = self.load_csv_data("Device_Status_Table.csv")
            
            # 1列目（Type）にダウンリストを追加
            for row in range(5):
                combo1 = QComboBox(self.table)
                combo1.addItems(self.type_list)  # CSVから読み込んだTypeのリストを使用
                self.table.setCellWidget(row, 0, combo1)  # 1列目にダウンリストを配置

            # 5列目（Query）にダウンリストを追加
            for row in range(5):
                combo2 = QComboBox(self.table)
                combo2.addItems(self.query_list)  # CSVから読み込んだQueryのリストを使用
                self.table.setCellWidget(row, 4, combo2)  # 5列目にダウンリストを配置
            
            # 6列目（Run）に押しボタンをセルいっぱいに追加
            for row in range(5):
                run_button = QPushButton("Run", self.table)
                run_button.clicked.connect(lambda _, r=row: self.run_button_clicked(r))  # クリックイベントを設定
                self.table.setCellWidget(row, 5, run_button)  # 6列目にボタンを配置
                self.update_button_size(run_button, row, 5)  # ボタンのサイズを更新

            # 7列目（Enable）にチェックボックスを中央揃えで追加
            for row in range(5):
                checkbox = QCheckBox(self.table)
                checkbox_layout = QHBoxLayout()  # 中央揃え用のレイアウト
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)  # 中央揃えに設定
                checkbox_widget = QWidget()
                checkbox_widget.setLayout(checkbox_layout)
                self.table.setCellWidget(row, 6, checkbox_widget)  # 7列目にチェックボックスを配置
            
            # Num列（1列目）とElements列（2列目）にQLineEditを追加して数字のみを受け付けるようにする
            for row in range(5):
                # Num列（1列目）
                num_line_edit = QLineEdit(self.table)
                num_line_edit.setValidator(QtGui.QIntValidator())  # 数値のみを受け付ける
                self.table.setCellWidget(row, 1, num_line_edit)
                
                # Elements列（2列目）
                # elements_line_edit = QLineEdit(self.table)
                # elements_line_edit.setValidator(QtGui.QIntValidator())  # 数値のみを受け付ける
                # self.table.setCellWidget(row, 2, elements_line_edit)

            # StatusとString列にQTableWidgetItemを追加
            for row in range(5):
                # Status列（4番目の列）
                status_item = QTableWidgetItem("-----")
                self.table.setItem(row, 3, status_item)  # 4番目の列（Status列）にアイテムを追加
                # String列（7番目の列）
                string_item = QTableWidgetItem("-----")
                self.table.setItem(row, 7, string_item)  # 7番目の列（String列）にアイテムを追加

                # Status列（4番目の列）の書き込み禁止
                self.table.item(row, 3).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                # String列（7番目の列）の書き込み禁止
                self.table.item(row, 7).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            # 各列のリサイズモードを設定（列幅を調整できるようにする）
            for col in range(8):
                self.table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)  # 列幅調整可能に設定
            
            # 行追加ボタンを作成
            self.add_row_button = QPushButton("Add Row", self)
            self.add_row_button.clicked.connect(self.add_row)  # ボタンがクリックされたときに行を追加
            self.layout.addWidget(self.add_row_button)

            # テーブルをレイアウトに追加
            self.layout.addWidget(self.table)
        
        # コマンドログ用テキストボックス（Command Logにのみ追加）
        if not table_name:  # table_nameがない場合（Command Log用）
            self.text_edit = QTextEdit(self)
            self.text_edit.setPlaceholderText("Enter command log here...")
            self.text_edit.setReadOnly(True)  # 読み取り専用にする
            self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)

    def load_csv_data(self, filename):
        # CSVファイルを読み込んで、TypeとQuery列を取得
        type_list = []
        query_list = []
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # TypeとQueryの列をリストに追加
                if row['Type'] not in type_list:
                    type_list.append(row['Type'])
                if row['Query'] not in query_list:
                    query_list.append(row['Query'])
        return type_list, query_list
    
    def add_row(self):
        # 新しい行をテーブルに追加
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)  # 新しい行を挿入

        # 新しい行に対して、必要なウィジェット（QComboBox, QLineEdit, etc.）を追加
        num_line_edit = QLineEdit(self.table)
        num_line_edit.setValidator(QtGui.QIntValidator())
        self.table.setCellWidget(row_count, 1, num_line_edit)

        # elements_line_edit = QLineEdit(self.table)
        # elements_line_edit.setValidator(QtGui.QIntValidator())
        # self.table.setCellWidget(row_count, 2, elements_line_edit)

        combo1 = QComboBox(self.table)
        combo1.addItems(self.type_list)
        self.table.setCellWidget(row_count, 0, combo1)

        combo2 = QComboBox(self.table)
        combo2.addItems(self.query_list)
        self.table.setCellWidget(row_count, 4, combo2)

        run_button = QPushButton("Run", self.table)
        run_button.clicked.connect(lambda _, r=row_count: self.run_button_clicked(r))
        self.table.setCellWidget(row_count, 5, run_button)

        checkbox = QCheckBox(self.table)
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)
        checkbox_widget = QWidget()
        checkbox_widget.setLayout(checkbox_layout)
        self.table.setCellWidget(row_count, 6, checkbox_widget)

        status_item = QTableWidgetItem("-----")
        self.table.setItem(row_count, 3, status_item)

        string_item = QTableWidgetItem("-----")
        self.table.setItem(row_count, 7, string_item)

        # 新しい行の高さを50に設定
        self.table.setRowHeight(row_count, 50)

    def update_button_size(self, button, row, col):
        # ボタンのサイズを調整
        button.setFixedSize(self.table.columnWidth(col), self.table.rowHeight(row))

    def run_button_clicked(self, row):
        Device_type = self.table.cellWidget(row, 0)
        Device_num = self.table.cellWidget(row, 1)
        Device_query = self.table.cellWidget(row, 4)

        Type_value = Device_type.currentText() if Device_type else "Not Selected"
        Num_value = Device_num.text() if Device_num else "Not Provided"
        Query_value = Device_query.currentText() if Device_query else "Not Selected"

        if Query_value == 'Set':
            PLCdata = kv.set(Type_value + Num_value)
        
        elif Query_value == 'Reset':
            PLCdata = kv.reset(Type_value + Num_value)
        
        print(PLCdata)
        self.main_window.append_to_log(f"set(): {PLCdata}")

        self.main_window.append_to_log(f"Running command: Type={Type_value}, Num={Num_value}, Query={Query_value}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
