# import sys
# from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTabWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
# from PyQt5.QtGui import QIcon
# from PLC_CommandClass import *

# __program__ = 'PLC_Monitor'

# class MainWindow(QMainWindow):
    
#     def __init__(self):
#         super().__init__()
#         self.title = __program__
#         self.left = 1250
#         self.top = 100
#         self.width = 768
#         self.height = 1024
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.table_widget = CommandLogTable(self)
#         self.setCentralWidget(self.table_widget)

#         self.show()
    
# class CommandLogTable(QWidget):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)

        
#         # initialize tab screen
#         self.tabs = QTabWidget()
#         # self.tab1 = QWidget()
#         # self.tab2 = QWidget()
#         self.tab = []
#         self.tabs.resize(1200, 800)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     ui = MainWindow()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QTabWidget, QApplication, QVBoxLayout
from PyQt5.QtGui import QIcon
# from PLC_CommandClass import *  # 必要に応じてインポート

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
        
        # CommandLogTable をメインウィジェットとして設定
        self.table_widget = CommandLogTable(self)
        self.setCentralWidget(self.table_widget)

        self.show()
    
class CommandLogTable(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # タブウィジェットを初期化
        self.tabs = QTabWidget()
        
        # 各タブの作成
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        # タブにテーブルを追加
        self.createTable(self.tab1, "Table 1")
        self.createTable(self.tab2, "Table 2")
        
        # タブを追加
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        
        # タブウィジェットをレイアウトに追加
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def createTable(self, tab, table_name):
        # QTableWidgetを作成
        table = QTableWidget()
        table.setRowCount(5)       # 行数を設定
        table.setColumnCount(3)    # 列数を設定
        table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        
        # テーブルにデータを追加
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"{table_name} - Item {row+1},{col+1}")
                table.setItem(row, col, item)
        
        # テーブルをタブのレイアウトに追加
        tab.layout = QVBoxLayout()
        tab.layout.addWidget(table)
        tab.setLayout(tab.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
