from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect,
                             QScrollArea, QDialog,QPushButton,QSplitter,QSizePolicy)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from .individual_dashboard import IndividualDashboard
import pandas as pd
import os
from utils.json_logic import *
from .cash_flow import CashFlowNetwork
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot
import json
from functools import partial

class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                text-align: left;
                padding: 8px 15px;
                border-radius: 5px;
                margin: 2px 10px;
            }
            QPushButton:checked {
                background-color: #e0e7ff;
                color: #4338ca;
            }
            QPushButton:hover:!checked {
                background-color: #f3f4f6;
            }
        """)


class CaseDashboard(QWidget):
    def __init__(self,case_id):
        super().__init__()
        self.case_id = case_id
        self.case = load_case_data(case_id)
        print("self.case",self.case)
        self.case_result = load_result(self.case_id)
        self.buttons = {}  # Store buttons for management
        self.section_widgets = {}  # Store section widgets
        self.current_section_label = None  # Store current section label

        self.init_ui()

    def init_ui(self):
        self.showFullScreen()  # Make window fullscreen

         # Create main widget and layout
        main_widget = QWidget()
        # self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create sidebar
        sidebar = self.createSidebar()
        
        # Create content area
        content_area = self.createContentArea()

        # Add splitter for resizable sidebar
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(sidebar)
        splitter.addWidget(content_area)
        splitter.setStretchFactor(splitter.indexOf(content_area), 1)
        splitter.setStretchFactor(0, 0)  # Sidebar gets minimal stretch
        splitter.setStretchFactor(1, 1)  # Content area stretches with the window
        splitter.setSizes([250, 1150])  # Initial sizes
            
        main_layout.addWidget(splitter,stretch=1)

        # Set default section to open
        self.showSection("Fund Flow Network Graph", self.create_network_graph())

        # Title
        # title = QLabel("Case Dashboard Overview")
        # title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        # title.setStyleSheet("color: #2c3e50;")
        # content_layout.addWidget(title)

        # Fund Flow Chart
        # content_layout.addWidget(self.create_section_title("Fund Flow Chart"))
        # content_layout.addWidget(self.create_network_graph())
        
        # Entity Distribution Chart
        # content_layout.addWidget(self.create_section_title("Entity Distribution"))
        # content_layout.addWidget(self.create_entity_distribution_chart(self.case_result))

        # # Individual Table
        # content_layout.addWidget(self.create_section_title("Individual Person Table"))
        # content_layout.addWidget(self.create_dummy_data_table_individual())

        # Link analysis
        # link_analysis_table = DynamicDataTable(
        #     df=self.case_result["cummalative_df"]["link_analysis_df"],
        #     title="Link Analysis Data Table",  # Optional
        #     rows_per_page=10  # Optional
        # )

        # # Add it to your layout
        # link_analysis_table.create_table(content_layout)
        
        # Bidirectional analysis
        # bidirectional_analysis_table = DynamicDataTable(
        #     df=self.case_result["cummalative_df"]["bidirectional_analysis"],
        #     title="Bidirectional Analysis Data Table",  # Optional
        #     rows_per_page=10  # Optional
        # )

        # Add it to your layout
        # bidirectional_analysis_table.create_table(content_layout)

        # # Entity Table
        # content_layout.addWidget(self.create_section_title("Entity Table"))
        # content_layout.addWidget(self.create_dummy_data_table_entity())

        # Set content widget in scroll area
        self.setLayout(main_layout)
    
    def createSidebar(self):
        sidebar = QWidget()
        sidebar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)  # Prevents sidebar from expanding unnecessarily
        sidebar.setMaximumWidth(300)
        sidebar.setMinimumWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)
        
        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #f8fafc;")
        header_layout = QVBoxLayout(header)
        
        title = QLabel("Case Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
        subtitle = QLabel(f"Case ID: {self.case_id}")
        subtitle.setStyleSheet("color: #64748b;padding:4px 0;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        sidebar_layout.addWidget(header)
        
       
        self.categories = {
            "Fund Flow Network Graph": self.create_network_graph(),
            "Entites Distribution": self.create_entity_distribution_chart(self.case_result),
            "Individual Table": self.create_dummy_data_table_individual(),
            "Link Analysis": self.create_link_analysis(),
        }
    
    # Create buttons for each category
        for category, widget_class in self.categories.items():
            # Create button for each category
            btn = SidebarButton(category)
            btn.clicked.connect(partial(self.showSection, category, widget_class))
            self.buttons[category] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        return sidebar
   
    def createContentArea(self):
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Header bar
        header = QWidget()
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #e2e8f0;")
        header_layout = QHBoxLayout(header)
        
        self.current_section_label = QLabel("Bank Transactions")
        self.current_section_label.setStyleSheet("font-size: 24px; font-weight: bold; color:#1e293b;opacity:0.8;padding: 5px 0;")
        self.current_section_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
        header_layout.addWidget(self.current_section_label)
        
        content_layout.addWidget(header)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8fafc;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f1f5f9;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # # Content container
        # self.content_stack = QStackedWidget()
        # scroll.setWidget(self.content_stack)
        
        # # Wrap scroll area in a layout to maintain padding and spacing
        # scroll_layout = QVBoxLayout()

        # scroll_layout.setContentsMargins(0, 0, 0, 100)
        # scroll_layout.addWidget(scroll)
        # content_layout.addLayout(scroll_layout)
        
        # return content_widget
        # Create a widget to hold all the content
        self.content_container = QWidget()
        # make content_container take all the height available

        self.content_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.content_container)
        content_layout.addWidget(scroll,stretch=1)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        
        return content_widget
        
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
            QTableWidget::setItem {
                text-align: center;
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
        data = []
        for i in range(len(self.case["individual_names"]["Name"])):
            data.append({ "Name": self.case["individual_names"]["Name"][i], "Account Number": self.case["individual_names"]["Acc Number"][i], "Pdf Path": self.case["file_names"][i]})
        headers = ["Name","Account Number","Pdf Path"]
        table_widget = PaginatedTableWidget(headers, data, rows_per_page=10,case_id=self.case_id)
        
        self.add_shadow(table_widget)
        return table_widget
    
    def create_table_individual(self):
        data = []
        for i in range(len(self.case["individual_names"]["Name"])):
            data.append({
                "ID": i+1, 
                "Name": self.case["individual_names"]["Name"][i], 
                "Account Number": self.case["individual_names"]["Acc Number"][i], 
                "Pdf Path": self.case["file_names"][i]
            })
        table_widget = IndividualTableWidget(data=data, case_id=self.case_id)
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
        table_widget = PaginatedTableWidget(headers, dummy_data,case_id=self.case_id, rows_per_page=10)
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

    def filter_transactions_by_frequency(self,result):
        # Get the process_df and entity frequency dataframe
        process_df = result["cummalative_df"]["process_df"]
        entity_freq_df = result["cummalative_df"]["entity_df"]
        
        # Convert entity frequency data to a dictionary for easier lookup
        # Assuming the first column is 'Entity' and second is 'Frequency'
        entity_freq_dict = dict(zip(entity_freq_df.iloc[:, 0], entity_freq_df.iloc[:, 1]))
        
        # Get base filtered dataframe with required columns and non-null entities
        filtered_df = process_df[['Name', 'Value Date', 'Debit', 'Credit', 'Entity']].dropna(subset=['Entity'])
        
        # Filter based on entity frequency
        # min_frequency = 30
        # filtered_df = filtered_df[filtered_df['Entity'].map(lambda x: entity_freq_dict.get(x, 0) > min_frequency)]
        
        return CashFlowNetwork(data=filtered_df)
    
    def create_network_graph(self):
        try:
            # df = result["cummalative_df"]["process_df"]
            # filtered_df = df[['Name', "Value Date",'Debit', 'Credit', 'Entity']].dropna(subset=['Entity'])
            # threshold = 10000
            # filtered_df = df[(df['Debit'] >= threshold) | (df['Credit'] >= threshold)]
            # return CashFlowNetwork(data=filtered_df)
            return self.filter_transactions_by_frequency(self.case_result)
        
        except Exception as e:
            print("Error",e)
            # import a excel
            df  = pd.read_excel("src/data/network_process_df.xlsx")
            filtered_df = df[['Name', "Value Date",'Debit', 'Credit', 'Entity']].dropna(subset=['Entity'])
            threshold = 10000
            filtered_df = df[(df['Debit'] >= threshold) | (df['Credit'] >= threshold)]
            return CashFlowNetwork(data=filtered_df)
        
    def create_entity_distribution_chart(self,result):
        try:
            entity_df = result["cummalative_df"]["entity_df"]
            # Remove rows where Entity is empty
            entity_df = entity_df[entity_df.iloc[:, 0] != ""]
            # Take top 10 entities by frequency
            entity_df_10 = entity_df.nlargest(10, entity_df.columns[1])
            return EntityDistributionChart(data={"piechart_data":entity_df_10,"table_data":entity_df,"all_transactions":result["cummalative_df"]["process_df"]})
        except Exception as e:
            print("Error creating entity distribution chart:", e)
            # Create dummy data if there's an error
            dummy_data = pd.DataFrame({
                'Entity': ['Entity1', 'Entity2', 'Entity3'],
                'Frequency': [10, 8, 6]
            })
            return EntityDistributionChart(data={"piechart_data":dummy_data,"table_data":dummy_data,"all_transactions":pd.DataFrame()})
    
    # def create_link_analysis(self,content_layout):
    def create_link_analysis(self):
        link_analysis_table = DynamicDataTable(
            df=self.case_result["cummalative_df"]["link_analysis_df"],
            # title="Link Analysis Data Table",  # Optional
            rows_per_page=10  # Optional
        )
        # link_analysis_table.create_table(content_layout)
        return link_analysis_table.create_table()

    def showSection(self, section_name, widget_class):
        # Uncheck all buttons except the clicked one
        for btn in self.buttons.values():
            btn.setChecked(False)
        self.buttons[section_name].setChecked(True)

        # Update the section label
        self.current_section_label.setText(section_name)

        # # Clear previous content
        # while self.content_layout.count():
        #     item = self.content_layout.takeAt(0)
        #     print("Item ",section_name," - ", item)
        #     print("Item widget ",section_name," - ", item.widget())
        #     if item.widget():
        #         item.widget().deleteLater()

        # Check if the widget for this section already exists
        if section_name in self.section_widgets:
            widget = self.section_widgets[section_name]
        else:
            widget = widget_class
            self.section_widgets[section_name] = widget

        # Set expanding size policy to adjust according to content
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Clear the content layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        # Add the widget to the content layout
        self.content_layout.addWidget(widget)
        
        # Add stretch at the bottom to push content to the top and allow scroll if necessary
        self.content_layout.addStretch()

class PaginatedTableWidget(QWidget):
    def __init__(self, headers, data, case_id,rows_per_page=10):
        super().__init__()
        self.headers = headers
        self.all_data = data
        self.rows_per_page = rows_per_page
        self.current_page = 0
        self.case_id = case_id
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
        self.table.verticalHeader().setVisible(False)
        
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
            QTableWidget::setItem {
                text-align: center; !important /* Center text in cells */
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
        self.prev_button.setStyleSheet(self.button_styles())
        
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("color: #34495e; font-weight: bold; font-size: 14px;")
        
        # Next page button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setStyleSheet(self.button_styles())
        
        # Add widgets to pagination layout
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch()
        
        # Add widgets to main layout
        layout.addWidget(self.table)
        layout.addLayout(pagination_layout)
        
        # Initial load
        self.update_table()
        
        # Connect cell click signal
        self.table.cellClicked.connect(self.on_cell_click)
    
    def button_styles(self):
        return """
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
        """
    
    def update_table(self):
        start_idx = self.current_page * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, len(self.all_data))
        
        self.table.setRowCount(self.rows_per_page)
        self.table.clearContents()
        
        for row, data in enumerate(self.all_data[start_idx:end_idx]):
            for col, key in enumerate(data.keys()):
                item = QTableWidgetItem(str(data[key]))
                
                # Center align the ID column
                if key == "ID":
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                self.table.setItem(row, col, item)
        
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
            if column == 1:
                name = self.all_data[actual_row]["Name"]
                print(f"Clicked on name: {name}")
                print("row",row)
                cash_flow_network = IndividualDashboard(case_id=self.case_id,name=name,row_id=row)
                # Create a new dialog and set the CashFlowNetwork widget as its central widget
                self.new_window = QDialog(self)
                self.new_window.setModal(False)  # Set the dialog as non-modal

                # Set the minimum size of the dialog
                # self.new_window.setMinimumSize(1000, 800)  # Set the minimum width and height
                # make the dialog full screen
                self.new_window.showMaximized()
                # show minimize and resize option on the Qdialog window
                self.new_window.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint)
                self.new_window.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)
                self.new_window.setWindowFlag(Qt.WindowType.WindowCloseButtonHint)
                

                # Create a layout for the dialog and add the CashFlowNetwork widget
                layout = QVBoxLayout()
                layout.addWidget(cash_flow_network)
                self.new_window.setLayout(layout)

                # Show the new window
                self.new_window.show()

   
class EntityDistributionChart(QWidget):
    def __init__(self, data):
        super().__init__()
        self.piechart_data = data["piechart_data"]
        self.table_data = data["table_data"]
        self.all_transactions = data["all_transactions"]  # Store transactions DataFrame

        self.current_page = 1
        self.rows_per_page = 10
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create web view
        self.web = QWebEngineView()
        layout.addWidget(self.web)
        
        # Process data for chart
        piechart_data = {}
        for _, row in self.piechart_data.iterrows():
            piechart_data[str(row.iloc[0])] = int(row.iloc[1])

        # Process data for chart
        table_data = {}
        for _, row in self.table_data.iterrows():
            table_data[str(row.iloc[0])] = int(row.iloc[1])

        # Process transactions data for JavaScript
        transactions_by_entity = {}
        print("all_transactions",self.all_transactions.head())
        for entity in table_data.keys():
            # Filter transactions for this entity
            entity_transactions = self.all_transactions[
                self.all_transactions['Description'].str.contains(entity, case=False, na=False)
            ].copy()
            
            # Convert to list of dictionaries for JSON serialization
            transactions_list = []
            for _, trans in entity_transactions.iterrows():
                transactions_list.append({
                    'date': trans['Value Date'].strftime('%Y-%m-%d'),
                    'description': trans['Description'],
                    'debit': str(trans['Debit']) if not pd.isna(trans['Debit']) else '',
                    'credit': str(trans['Credit']) if not pd.isna(trans['Credit']) else '',
                    'category': trans['Category']
                })
            transactions_by_entity[entity] = transactions_list
        

        # Generate HTML content
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Entity Distribution</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .chart-container {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin: 20px;
                    min-height: 400px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .header {{
                    text-align: center;
                    padding: 10px;
                    color: #2c3e50;
                    font-size: 1.2em;
                    font-weight: bold;
                }}
                .table-container {{
                    margin: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                    border: 1px solid #e2e8f0; /* Add vertical line between cells */
                }}
                th, td {{
                    padding: 12px;
                    border-bottom: 1px solid #e2e8f0;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                    text-align: center;
                }}
                tr:hover {{
                    background-color: #f8fafc;
                }}
                .table-header {{
                    text-align: center;
                    padding: 10px;
                    color: #2c3e50;
                    font-size: 1.2em;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .pagination {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 20px;
                    gap: 10px;
                }}
                .pagination button {{
                    padding: 8px 16px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                }}
                .pagination button:disabled {{
                    background-color: #bdc3c7;
                    cursor: not-allowed;
                }}
                .pagination span {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                #entityChart {{
                    max-width: 100%;
                    height: 100%;
                }}
                .tr-list td {{
                    width: 50%;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    text-align: center;
                    cursor: pointer;
                }}
                .key{{
                    border-right: 1px solid #e2e8f0; /* Add vertical line between cells */
                }}
                .amount-cell {{
                    text-align: right;
                }}
                .amount-cell.debit {{
                    color: #e74c3c;
                }}
                .amount-cell.credit {{
                    color: #27ae60;
                }}
                .close-button {{
                    background: #f1f5f9;
                    color: #64748b;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    transition: all 0.2s ease;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                    margin-left:auto;
                    margin-bottom: 10px;

                }}

                .close-button:hover {{
                    background: #e2e8f0;
                    color: #475569;
                }}

                .close-button::before {{
                    content: '✕';
                    font-size: 14px;
                    margin-right: 4px;
                }}

            </style>
        </head>
        <body>
            <div class="header">Top 10 Entities by Transaction Frequency</div>
            <div class="chart-container">
                <canvas id="entityChart"></canvas>
            </div>
            
            <div class="table-container">
                <div class="table-header">Complete Entity Frequency List</div>
                <table>
                    <thead>
                        <tr>
                            <th>Entity</th>
                            <th>Frequency</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                    </tbody>
                </table>
                <div class="pagination">
                    <button id="prevBtn" onclick="previousPage()">Previous</button>
                    <span id="pageInfo"></span>
                    <button id="nextBtn" onclick="nextPage()">Next</button>
                </div>
            </div>

            <div id="table-container-nested">
            </div>

            
            <script>
                const piechart_data = {json.dumps(piechart_data)};
                const table_data = {json.dumps(table_data)};
                const transactionsByEntity = {json.dumps(transactions_by_entity)};
                let currentTransactionsPage = 1;
                const transactionsPerPage = 10;
                let currentEntityTransactions = [];


                const colors = [
                    '#10B981', '#6366F1', '#F59E0B', '#D946EF', '#0EA5E9',
                    '#34D399', '#8B5CF6', '#EC4899', '#F97316', '#14B8A6'
                ];
                
                // Pie Chart
                const ctx = document.getElementById('entityChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'pie',
                    data: {{
                        labels: Object.keys(piechart_data),
                        datasets: [{{
                            data: Object.values(piechart_data),
                            backgroundColor: colors,
                            borderColor: '#ffffff',
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'right',
                                labels: {{
                                    padding: 20,
                                    font: {{
                                        size: 12,
                                        family: "'Segoe UI', sans-serif"
                                    }},
                                    generateLabels: function(chart) {{
                                        const data = chart.data;
                                        const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                                        return data.labels.map((label, i) => {{
                                            const value = data.datasets[0].data[i];
                                            const percentage = ((value / total) * 100).toFixed(1);
                                            return {{
                                                text: `${{label}} (${{percentage}}%)`,
                                                fillStyle: colors[i],
                                                strokeStyle: colors[i],
                                                lineWidth: 0,
                                                hidden: false,
                                                index: i
                                            }};
                                        }});
                                    }}
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const value = context.raw;
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return `${{context.label}}: ${{value}} transactions (${{percentage}}%)`;
                                    }}
                                }}
                            }}
                        }},
                        layout: {{
                            padding: 20
                        }},
                        animation: {{
                            animateScale: true,
                            animateRotate: true
                        }}
                    }}
                }});

                // Table Pagination
                const rowsPerPage = 10;
                let currentPage = 1;
                const data = Object.entries(table_data).sort((a, b) => b[1] - a[1]);
                const totalPages = Math.ceil(data.length / rowsPerPage);

                function updateTable() {{
                    const start = (currentPage - 1) * rowsPerPage;
                    const end = start + rowsPerPage;
                    const pageData = data.slice(start, end);
                    
                    const tableBody = document.getElementById('tableBody');
                    tableBody.innerHTML = '';
                    
                    pageData.forEach(([entity, frequency]) => {{
                        const row = `
                            <tr class="tr-list" onclick="showTransactionTable('${{entity}}')">
                                <td class="key">${{entity}}</td>
                                <td>${{frequency}}</td>
                            </tr>
                        `;
                        tableBody.innerHTML += row;
                    }});
                    
                    document.getElementById('pageInfo').textContent = `Page ${{currentPage}} of ${{totalPages}}`;
                    document.getElementById('prevBtn').disabled = currentPage === 1;
                    document.getElementById('nextBtn').disabled = currentPage === totalPages;
                }}

                function updateTransactionsTable(entity) {{
                    const start = (currentTransactionsPage - 1) * transactionsPerPage;
                    const end = start + transactionsPerPage;
                    const pageTransactions = currentEntityTransactions.slice(start, end);
                    const totalTransactionsPages = Math.ceil(currentEntityTransactions.length / transactionsPerPage);
                    
                    const transactionTableHtml = `
                        <div class="table-container">
                            <div class="table-header-container">
                                <div class="table-header">Transactions for ${entity}</div>
                                <button class="close-button" onclick="closeTransactionTable()">Close</button>
                            </div>
                            <table class="transaction-table">
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Description</th>
                                        <th>Debit</th>
                                        <th>Credit</th>
                                        <th>Category</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${{pageTransactions.map(t => `
                                        <tr>
                                            <td>${{t.date}}</td>
                                            <td>${{t.description}}</td>
                                            <td class="amount-cell debit">${{t.debit}}</td>
                                            <td class="amount-cell credit">${{t.credit}}</td>
                                            <td>${{t.category}}</td>
                                        </tr>
                                    `).join('')}}
                                </tbody>
                            </table>
                            <div class="pagination">
                                <button onclick="previousTransactionsPage('${{entity}}')" ${{currentTransactionsPage === 1 ? 'disabled' : ''}}>Previous</button>
                                <span>Page ${{currentTransactionsPage}} of ${{totalTransactionsPages}}</span>
                                <button onclick="nextTransactionsPage('${{entity}}')" ${{currentTransactionsPage === totalTransactionsPages ? 'disabled' : ''}}>Next</button>
                            </div>
                        </div>
                    `;

                    document.getElementById('table-container-nested').innerHTML = transactionTableHtml;
                }}

                function showTransactionTable(entity) {{
                    const transactions = transactionsByEntity[entity] || [];
                    currentEntityTransactions = transactions;
                    currentTransactionsPage = 1;
                    
                   if (transactions.length === 0) {{
                        document.getElementById('table-container-nested').innerHTML = `
                            <div class="table-container">
                                <div class="table-header-container">
                                    <div class="table-header">No transactions found for ${entity}</div>
                                    <button class="close-button" onclick="closeTransactionTable()">Close</button>
                                </div>
                            </div>
                        `;
                        return;
                    }}
                    
                    updateTransactionsTable(entity);
                }}

                function previousTransactionsPage(entity) {{
                    if (currentTransactionsPage > 1) {{
                        currentTransactionsPage--;
                        updateTransactionsTable(entity);
                    }}
                }}

                function nextTransactionsPage(entity) {{
                    const totalPages = Math.ceil(currentEntityTransactions.length / transactionsPerPage);
                    if (currentTransactionsPage < totalPages) {{
                        currentTransactionsPage++;
                        updateTransactionsTable(entity);
                    }}
                }}

                
                function closeTransactionTable() {{
                    document.getElementById('table-container-nested').innerHTML = '';
                }}
                
                function nextPage() {{
                    if (currentPage < totalPages) {{
                        currentPage++;
                        updateTable();
                    }}
                }}

                function previousPage() {{
                    if (currentPage > 1) {{
                        currentPage--;
                        updateTable();
                    }}
                }}

                // Initial table load
                updateTable();
            </script>
        </body>
        </html>
        '''
        
        self.web.setMinimumHeight(2100)  # Set minimum height instead of fixed height
        self.web.setHtml(html_content)

class IndividualTableWidget(QWidget):
    def __init__(self, data, case_id):
        super().__init__()
        self.all_data = data
        self.case_id = case_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create web view
        self.web = QWebEngineView()
        layout.addWidget(self.web)
        
        # Convert data to format needed for JavaScript
        table_data = []
        for item in self.all_data:
            table_data.append({
                'id': item['ID'],
                'name': item['Name'],
                'account': item['Account Number'],
                'pdf': item['Pdf Path']
            })

        # Generate HTML content
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Individual Person Table</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/qt-webengine-channel/6.4.0/qwebchannel.js"></script>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .table-container {{
                    margin: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th, td {{
                    padding: 12px;
                    border-bottom: 1px solid #e2e8f0;
                    border-right: 1px solid #e2e8f0;
                }}
                th:last-child, td:last-child {{
                    border-right: none;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                }}
                tr:hover {{
                    background-color: #f8fafc;
                    cursor: pointer;
                }}
                .table-header {{
                    text-align: center;
                    padding: 10px;
                    color: #2c3e50;
                    font-size: 1.2em;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .pagination {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 20px;
                    gap: 10px;
                }}
                .pagination button {{
                    padding: 8px 16px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                }}
                .pagination button:disabled {{
                    background-color: #bdc3c7;
                    cursor: not-allowed;
                }}
                .pagination span {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .tr-list td {{
                    text-align: center;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }}
                .clickable-name {{
                    color: #3498db;
                    text-decoration: underline;
                    cursor: pointer;
                }}
                .clickable-name:hover {{
                    color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="table-container">
                <div class="table-header">Individual Person List</div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Account Number</th>
                            <th>PDF Path</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                    </tbody>
                </table>
                <div class="pagination">
                    <button id="prevBtn" onclick="previousPage()">Previous</button>
                    <span id="pageInfo"></span>
                    <button id="nextBtn" onclick="nextPage()">Next</button>
                </div>
            </div>
            
            <script>
                let qt = null;

                const data = {table_data};
                const rowsPerPage = 10;
                let currentPage = 1;
                const totalPages = Math.ceil(data.length / rowsPerPage);

                function handleNameClick(name) {{
                    if (qt) {{
                        qt.nameClicked(name);
                    }}
                }}

                function updateTable() {{
                    const start = (currentPage - 1) * rowsPerPage;
                    const end = start + rowsPerPage;
                    const pageData = data.slice(start, end);
                    
                    const tableBody = document.getElementById('tableBody');
                    tableBody.innerHTML = '';
                    
                    pageData.forEach(item => {{
                        const row = `
                            <tr class="tr-list">
                                <td>${{item.id}}</td>
                                <td class="clickable-name" onclick="handleNameClick('${{item.name}}')">${{item.name}}</td>
                                <td>${{item.account}}</td>
                                <td>${{item.pdf}}</td>
                            </tr>
                        `;
                        tableBody.innerHTML += row;
                    }});
                    
                    document.getElementById('pageInfo').textContent = `Page ${{currentPage}} of ${{totalPages}}`;
                    document.getElementById('prevBtn').disabled = currentPage === 1;
                    document.getElementById('nextBtn').disabled = currentPage === totalPages;
                }}

                function nextPage() {{
                    if (currentPage < totalPages) {{
                        currentPage++;
                        updateTable();
                    }}
                }}

                function previousPage() {{
                    if (currentPage > 1) {{
                        currentPage--;
                        updateTable();
                    }}
                }}

                updateTable();
            </script>
        </body>
        </html>
        '''
        
        # Set minimum height for the web view
        self.web.setMinimumHeight(600)
        class Handler(QObject):
            def __init__(self, case_id, parent=None):
                super().__init__(parent)
                self.case_id = case_id
                self.parent_widget = parent

            @pyqtSlot(str)
            def nameClicked(self, name):
                dialog = QDialog(self.parent_widget)
                dialog.setWindowTitle("Individual Dashboard")
                dialog.showMaximized()
                dialog.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint)
                dialog.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)
                dialog.setWindowFlag(Qt.WindowType.WindowCloseButtonHint)
                
                layout = QVBoxLayout()
                individual_dashboard = IndividualDashboard(case_id=self.case_id, name=name, row_id=0)
                layout.addWidget(individual_dashboard)
                dialog.setLayout(layout)
                dialog.show()
        
        # Create channel and handler
        channel = QWebChannel()
        handler = Handler(parent=self, case_id=self.case_id)
        channel.registerObject('qt', handler)
        self.web.page().setWebChannel(channel)
        
        # Load the HTML content
        self.web.setHtml(html_content)


def create_data_table_reversal(self, layout):
    web_view = QWebEngineView()
    
    # Prepare table data
    table_data = []
    for _, row in self.df.iterrows():
        table_data.append({
            'date': str(row["Value Date"]),
            'description': row["Description"][:50] + "...",
            'debit': f"{float(row['Debit']) if pd.notna(row['Debit']) else 0:.2f}",
            'credit': f"{float(row['Credit']) if pd.notna(row['Credit']) else 0:.2f}",
            'balance': f"{float(row['Balance']):,.2f}",
            'category': row["Category"]
        })

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reversal Data</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
        .table-container {{
                margin: 20px;
                background: white;
                border-radius: 10px;
                padding: 20px;
                overflow: hidden;
            }}
        .table-header {{
                text-align: center;
                padding: 10px;
                color: #2c3e50;
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            
            th, td {{
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #e2e8f0;
            }}
            
            th {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
                position: sticky;
                top: 0;
                padding: 6px;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .description-column {{
                text-align: left;
            }}
        .pagination {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 20px;
                gap: 10px;
            }}
        .pagination button {{
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }}
        .pagination button:disabled {{
                background-color: #bdc3c7;
                cursor: not-allowed;
            }}
        .pagination span {{
                font-weight: bold;
                color: #333333;
            }}
        </style>
    </head>
    <body>
        <div class="table-container">
            <div class="table-header">Reversal Data Table</div>
            <table>
                <thead>
                    <tr>
                        <th>Value Date</th>
                        <th class="description-column">Description</th>
                        <th>Debit</th>
                        <th>Credit</th>
                        <th>Balance</th>
                        <th>Category</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                </tbody>
            </table>
            <div class="pagination">
                <button id="prevBtn" onclick="previousPage()">Previous</button>
                <span id="pageInfo"></span>
                <button id="nextBtn" onclick="nextPage()">Next</button>
            </div>
        </div>
        
        <script>
            const rowsPerPage = 10;
            let currentPage = 1;
            const data = {json.dumps(table_data)};
            const totalPages = Math.ceil(data.length / rowsPerPage);
            

            function updateTable() {{
                const start = (currentPage - 1) * rowsPerPage;
                const end = start + rowsPerPage;
                const pageData = data.slice(start, end);
                
                const tableBody = document.getElementById('tableBody');
                tableBody.innerHTML = '';
                
                pageData.forEach(row => {{
                    const tr = `
                        <tr>
                            <td>${{row.date}}</td>
                            <td class="description-column">${{row.description}}</td>
                            <td>${{row.debit}}</td>
                            <td>${{row.credit}}</td>
                            <td>${{row.balance}}</td>
                            <td>${{row.category}}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += tr;
                }});
                
                document.getElementById('pageInfo').textContent = `Page ${{currentPage}} of ${{totalPages}}`;
                document.getElementById('prevBtn').disabled = currentPage === 1;
                document.getElementById('nextBtn').disabled = currentPage === totalPages;
            }}

            function nextPage() {{
                if (currentPage < totalPages) {{
                    currentPage++;
                    updateTable();
                }}
            }}

            function previousPage() {{
                if (currentPage > 1) {{
                    currentPage--;
                    updateTable();
                }}
            }}

            // Initial table load
            updateTable();
        </script>
    </body>
    </html>
    '''
    
    web_view.setHtml(html_content)
    web_view.setFixedHeight(800)  # Set minimum height for the table
    layout.addWidget(web_view)

from PyQt6.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import json

class DynamicDataTable:
    def __init__(self, df, title="", rows_per_page=10):
        """
        Initialize the dynamic table with a DataFrame.
        
        Args:
            df (pandas.DataFrame): The DataFrame to display
            title (str): Title of the table
            rows_per_page (int): Number of rows to display per page
        """
        self.df = df
        self.title = title
        self.rows_per_page = rows_per_page

    # def create_table(self, layout):
    def create_table(self):
        """Create and add the table to the given layout."""
        web_view = QWebEngineView()
        
        # Convert DataFrame to table data
        table_data = []
        for _, row in self.df.iterrows():
            row_dict = {}
            for column in self.df.columns:
                value = row[column]
                
                # Handle different data types
                if pd.isna(value):
                    row_dict[column] = ""
                elif isinstance(value, (int, float)):
                    if column.lower() in ['debit', 'credit', 'balance', 'amount']:
                        row_dict[column] = f"{float(value):,.2f}"
                    else:
                        row_dict[column] = str(value)
                elif isinstance(value, pd.Timestamp):
                    row_dict[column] = value.strftime('%Y-%m-%d')
                else:
                    # Truncate long text
                    if isinstance(value, str) and len(value) > 50:
                        row_dict[column] = value[:50] + "..."
                    else:
                        row_dict[column] = str(value)
            
            table_data.append(row_dict)

        # Generate column headers with proper formatting
        columns = self.df.columns
        column_headers = []
        for col in columns:
            # Convert column names to proper format
            header = col.replace('_', ' ').title()
            column_headers.append({
                'id': col,
                'name': header,
                'align': 'left' if isinstance(self.df[col].iloc[0], str) else 'center'
            })

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.title}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .table-container {{
                    margin: 20px;
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .table-header {{
                    text-align: center;
                    padding: 15px;
                    color: #2c3e50;
                    font-size: 1.2rem;
                    font-weight: bold;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #eef2f7;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th, td {{
                    padding: 12px;
                    border-bottom: 1px solid #e2e8f0;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                    position: sticky;
                    top: 0;
                    padding: 12px;
                }}
                tr:hover {{
                    background-color: #f8fafc;
                    transition: background-color 0.2s ease;
                }}
                .text-left {{
                    text-align: left;
                }}
                .text-center {{
                    text-align: center;
                }}
                .pagination {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: 20px;
                    padding: 10px 0;
                    border-top: 1px solid #e2e8f0;
                }}
                .pagination-controls {{
                    display: flex;
                    gap: 10px;
                    align-items: center;
                }}
                .pagination button {{
                    padding: 8px 16px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: background-color 0.2s ease;
                }}
                .pagination button:hover {{
                    background-color: #2980b9;
                }}
                .pagination button:disabled {{
                    background-color: #bdc3c7;
                    cursor: not-allowed;
                }}
                .pagination-info {{
                    font-weight: bold;
                    color: #333333;
                }}
                .empty-table {{
                    text-align: center;
                    padding: 40px;
                    color: #666;
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            <div class="table-container">
                <div class="table-header">{self.title}</div>
                <table>
                    <thead>
                        <tr>
                            {
                                ''.join([
                                    f'<th class="{"text-left" if col["align"] == "left" else "text-center"}">{col["name"]}</th>'
                                    for col in column_headers
                                ])
                            }
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                    </tbody>
                </table>
                <div class="pagination">
                    <div class="pagination-info">
                        <span id="totalRecords"></span>
                    </div>
                    <div class="pagination-controls">
                        <button id="prevBtn" onclick="previousPage()">Previous</button>
                        <span id="pageInfo"></span>
                        <button id="nextBtn" onclick="nextPage()">Next</button>
                    </div>
                </div>
            </div>
            
            <script>
                const rowsPerPage = {self.rows_per_page};
                let currentPage = 1;
                const data = {json.dumps(table_data)};
                const columns = {json.dumps([col['id'] for col in column_headers])};
                const columnAlignments = {json.dumps({col['id']: col['align'] for col in column_headers})};
                const totalPages = Math.ceil(data.length / rowsPerPage);
                
                function updateTable() {{
                    const start = (currentPage - 1) * rowsPerPage;
                    const end = start + rowsPerPage;
                    const pageData = data.slice(start, end);
                    
                    const tableBody = document.getElementById('tableBody');
                    tableBody.innerHTML = '';
                    
                    if (data.length === 0) {{
                        tableBody.innerHTML = `
                            <tr>
                                <td colspan="${{columns.length}}" class="empty-table">
                                    No data available
                                </td>
                            </tr>
                        `;
                    }} else {{
                        pageData.forEach(row => {{
                            const tr = document.createElement('tr');
                            
                            columns.forEach(column => {{
                                const td = document.createElement('td');
                                td.className = columnAlignments[column] === 'left' ? 'text-left' : 'text-center';
                                td.textContent = row[column] || '';
                                tr.appendChild(td);
                            }});
                            
                            tableBody.appendChild(tr);
                        }});
                    }}
                    
                    document.getElementById('pageInfo').textContent = 
                        `Page ${{currentPage}} of ${{totalPages}}`;
                    document.getElementById('totalRecords').textContent = 
                        `Total Records: ${{data.length}}`;
                    document.getElementById('prevBtn').disabled = currentPage === 1;
                    document.getElementById('nextBtn').disabled = currentPage === totalPages;
                }}

                function nextPage() {{
                    if (currentPage < totalPages) {{
                        currentPage++;
                        updateTable();
                    }}
                }}

                function previousPage() {{
                    if (currentPage > 1) {{
                        currentPage--;
                        updateTable();
                    }}
                }}

                // Initial table load
                updateTable();
            </script>
        </body>
        </html>
        '''
        
        web_view.setHtml(html_content)
        web_view.setMinimumHeight(800)
        return web_view
        # layout.addWidget(web_view)