from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame,
                             QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect,
                             QScrollArea, QDialog,QComboBox,QPushButton)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from .cash_flow import CashFlowNetwork
import pandas as pd
import os

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create main layout for the scroll area
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the main content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Dashboard Overview")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        content_layout.addWidget(title)

        # Stats overview
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.report_count_widget = self.create_stat_widget("Total Reports", 10)  # Dummy value
        stats_layout.addWidget(self.report_count_widget)

        self.monthly_report_widget = self.create_stat_widget("Monthly Reports", 5)  # Dummy value
        stats_layout.addWidget(self.monthly_report_widget)

        self.active_users_widget = self.create_stat_widget("Active Users", 42)  # Dummy value
        stats_layout.addWidget(self.active_users_widget)

        content_layout.addLayout(stats_layout)

        # Individual Table
        content_layout.addWidget(self.create_section_title("Individual Person Table"))
        content_layout.addWidget(self.create_dummy_data_table_individual())

        # Entity Table
        content_layout.addWidget(self.create_section_title("Entity Table"))
        content_layout.addWidget(self.create_dummy_data_table_entity())

        # Set content widget in scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_stat_widget(self, label, value):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(widget)
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("color: #3498db;")
        
        desc_label = QLabel(label)
        desc_label.setFont(QFont("Arial", 14))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #7f8c8d;")
        
        layout.addWidget(value_label)
        layout.addWidget(desc_label)
        
        self.add_shadow(widget)
        return widget

    def create_section_title(self, title):
        label = QLabel(title)
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label.setStyleSheet("color: #2c3e50; margin-top: 20px;")
        return label

    def create_recent_reports_table(self):
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(["Date", "Report Name", "Status"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
        """)

        # Dummy data for demonstration
        recent_reports = [
            {"date": "2024-10-01", "name": "Report A", "status": "Complete"},
            {"date": "2024-10-02", "name": "Report B", "status": "Pending"},
            {"date": "2024-10-03", "name": "Report C", "status": "Complete"},
            {"date": "2024-10-04", "name": "Report D", "status": "Pending"},
            {"date": "2024-10-05", "name": "Report E", "status": "Complete"},
        ]

        for row, report in enumerate(recent_reports):
            table.setItem(row, 0, QTableWidgetItem(report['date']))
            table.setItem(row, 1, QTableWidgetItem(report['name']))
            table.setItem(row, 2, QTableWidgetItem(report['status']))

        self.add_shadow(table)
        return table

    def create_dummy_data_table_individual(self):
        # Extended dummy data
        dummy_data = [
            {"id": "1", "name": "Entry A", "status": "Active"},
            {"id": "2", "name": "Entry B", "status": "Inactive"},
            {"id": "3", "name": "Entry C", "status": "Active"},
            {"id": "4", "name": "Entry D", "status": "Inactive"},
            {"id": "5", "name": "Entry E", "status": "Active"},
            {"id": "6", "name": "Entry F", "status": "Active"},
            {"id": "7", "name": "Entry G", "status": "Inactive"},
            {"id": "8", "name": "Entry H", "status": "Active"},
            {"id": "9", "name": "Entry I", "status": "Inactive"},
            {"id": "10", "name": "Entry J", "status": "Active"},
            {"id": "11", "name": "Entry K", "status": "Inactive"},
            {"id": "12", "name": "Entry L", "status": "Active"},
        ]
        
        headers = ["ID", "Name", "Status"]
        table_widget = PaginatedTableWidget(headers, dummy_data, rows_per_page=10)
        self.add_shadow(table_widget)
        return table_widget

    def create_dummy_data_table_entity(self):
        # Extended dummy data
        dummy_data = [
            {"id": "1", "Entity Name": "Entry A", "status": "Active"},
            {"id": "2", "Entity Name": "Entry B", "status": "Inactive"},
            {"id": "3", "Entity Name": "Entry C", "status": "Active"},
            {"id": "4", "Entity Name": "Entry D", "status": "Inactive"},
            {"id": "5", "Entity Name": "Entry E", "status": "Active"},
            {"id": "6", "Entity Name": "Entry F", "status": "Active"},
            {"id": "7", "Entity Name": "Entry G", "status": "Inactive"},
            {"id": "8", "Entity Name": "Entry H", "status": "Active"},
            {"id": "9", "Entity Name": "Entry I", "status": "Inactive"},
            {"id": "10", "Entity Name": "Entry J", "status": "Active"},
            {"id": "11", "Entity Name": "Entry K", "status": "Inactive"},
            {"id": "12", "Entity Name": "Entry L", "status": "Active"},
        ]
        
        headers = ["Date", "Entity Name", "Status"]
        table_widget = PaginatedTableWidget(headers, dummy_data, rows_per_page=10)
        self.add_shadow(table_widget)
        return table_widget

    def on_cell_click(self, row, column):
        # Open a new window with the details of the clicked item
        dialog = QDialog(self)
        dialog.setWindowTitle("Entry Details")
        dialog_layout = QVBoxLayout(dialog)
        entry_label = QLabel(f"Details for Entry {row + 1}")
        entry_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        dialog_layout.addWidget(entry_label)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)

class PaginatedTableWidget(QWidget):
    def __init__(self, headers, data, rows_per_page=10):
        super().__init__()
        self.headers = headers
        self.all_data = data
        self.rows_per_page = rows_per_page
        self.current_page = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create table
        self.table = QTableWidget(self.rows_per_page, len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Disable scrollbars
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Calculate exact height needed for 10 rows plus header
        header_height = self.table.horizontalHeader().height()+20
        row_height = 35  # Set a fixed height for each row
        total_height = header_height + (row_height * self.rows_per_page)
        
        # Set row heights
        for i in range(self.rows_per_page):
            self.table.setRowHeight(i, row_height)
            
        # Set fixed table height
        self.table.setFixedHeight(total_height)
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
                color: black;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                color: black;
                padding: 5px;
            }
        """)

        # Create pagination controls
        pagination_layout = QHBoxLayout()
        
        
        
        # Previous page button
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        # Page information
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("color: #2c3e50; font-weight: bold; margin: 0 10px;")
        
        # Next page button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        # Add widgets to pagination layout
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        
        # Add widgets to main layout
        layout.addWidget(self.table)
        layout.addLayout(pagination_layout)
        
        # Initial load
        self.update_table()
        
        # Connect cell click signal
        self.table.cellClicked.connect(self.on_cell_click)

    def update_table(self):
        start_idx = self.current_page * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, len(self.all_data))
        
        self.table.setRowCount(self.rows_per_page)
        self.table.clearContents()
        
        for row, data in enumerate(self.all_data[start_idx:end_idx]):
            for col, key in enumerate(data.keys()):
                self.table.setItem(row, col, QTableWidgetItem(str(data[key])))
        
        total_pages = (len(self.all_data) + self.rows_per_page - 1) // self.rows_per_page
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages - 1)
        
    def next_page(self):
        self.current_page += 1
        self.update_table()
        
    def previous_page(self):
        self.current_page -= 1
        self.update_table()
        
    def change_rows_per_page(self, value):
        self.rows_per_page = int(value)
        self.current_page = 0
        
        # Recalculate height
        header_height = self.table.horizontalHeader().height()
        row_height = 35
        total_height = header_height + (row_height * self.rows_per_page)
        
        # Update table size
        self.table.setRowCount(self.rows_per_page)
        self.table.setFixedHeight(total_height)
        
        # Reset row heights
        for i in range(self.rows_per_page):
            self.table.setRowHeight(i, row_height)
            
        self.update_table()

    # def get_latest_excel_as_df(directory_path="/src/data/cummalative_excels"):
    #     # Step 1: List all Excel files in the directory
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     print("BASE_DIR",BASE_DIR)
    #     directory_path = os.path.join(BASE_DIR, directory_path)
    #     print("directory_path",directory_path)
    #     excel_files = [f for f in os.listdir(directory_path) if f.endswith(('.xlsx', '.xls'))]
        
    #     # Step 2: Identify the latest file based on the modification time
    #     if not excel_files:
    #         raise FileNotFoundError("No Excel files found in the specified directory.")

    #     latest_file = max(excel_files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
    #     latest_file_path = os.path.join(directory_path, latest_file)
        
    #     # Step 3: Load the latest Excel file into a DataFrame
    #     df = pd.read_excel(latest_file_path)
    #     return df

    def on_cell_click(self, row, column):
        start_idx = self.current_page * self.rows_per_page
        actual_row = start_idx + row
        if actual_row < len(self.all_data):
            dialog = QDialog()
            dialog.setWindowTitle("Cash Flow Network Graph")
            dialog_layout = QVBoxLayout(dialog)
            # TODO - go into the src/data/cummalative_excels and get the latest saved excel and convert that to df and send that to CashFlowNetwork as data
            # latest_df  = self.get_latest_excel_as_df()
            # dialog_layout.addWidget(CashFlowNetwork(data=latest_df))
            # dialog.setLayout(dialog_layout)
            # dialog.exec()
            # entry_label = QLabel(f"Details for Entry {self.all_data[actual_row]['id']}")
            # entry_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            # dialog_layout.addWidget(entry_label)
            # dialog.exec()