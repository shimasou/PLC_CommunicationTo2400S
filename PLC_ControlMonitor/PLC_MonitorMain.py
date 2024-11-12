import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QLabel, QTextEdit, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets  # 追加

__program__ = 'PLC_Monitor'

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

        self.show()
    
class CommandLogTable(QWidget):

    def __init__(self, parent, title, table_name=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
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
                self.table.setColumnWidth(col, 90)  # すべての列の幅を60pxに設定
            self.table.setColumnWidth(7, 300)

            # 行高さの初期設定
            for row in range(5):
                self.table.setRowHeight(row, 40)  # すべての行の高さを40pxに設定
            
            # テーブルにデータを追加
            for row in range(5):
                for col in range(8):
                    item = QTableWidgetItem(f"-----")
                    self.table.setItem(row, col, item)
            
            # 1列目（Type）にダウンリストを追加
            for row in range(5):
                combo1 = QComboBox(self.table)
                combo1.addItems(["", "Option 1", "Option 2", "Option 3"])  # 選択肢
                self.table.setCellWidget(row, 0, combo1)  # 1列目にダウンリストを配置

            # 5列目（Query）にダウンリストを追加
            for row in range(5):
                combo2 = QComboBox(self.table)
                combo2.addItems(["", "Query 1", "Query 2", "Query 3"])  # 選択肢
                self.table.setCellWidget(row, 4, combo2)  # 5列目にダウンリストを配置
            
            # 各列のリサイズモードを設定（列幅を調整できるようにする）
            for col in range(8):
                self.table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)  # 列幅調整可能に設定
            
            # テーブルをレイアウトに追加
            self.layout.addWidget(self.table)
        
        # コマンドログ用テキストボックス（Command Logにのみ追加）
        if not table_name:  # table_nameがない場合（Command Log用）
            self.text_edit = QTextEdit(self)
            self.text_edit.setPlaceholderText("Enter command log here...")
            self.text_edit.setReadOnly(True)  # 読み取り専用にする
            self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
