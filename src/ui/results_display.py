from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                            QTableWidgetItem, QLabel, QTabWidget)
from PyQt6.QtCore import Qt

class ResultsDisplay(QWidget):
    def __init__(self, result_data):
        super().__init__()
        self.result_data = result_data
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create tabs for different views
        tab_widget = QTabWidget()
        
        # Summary Tab
        summary_tab = self.create_summary_tab()
        tab_widget.addTab(summary_tab, "Summary")
        
        # Transactions Tab
        transactions_tab = self.create_transactions_tab()
        tab_widget.addTab(transactions_tab, "Transactions")
        
        # Analysis Tab
        analysis_tab = self.create_analysis_tab()
        tab_widget.addTab(analysis_tab, "Analysis")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
    
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Add summary information
        single_df = self.result_data["single_df"]
        for bank, data in single_df.items():
            layout.addWidget(QLabel(f"Bank: {bank}"))
            
            # Create summary table
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Metric", "Value"])
            
            # Add summary rows
            metrics = [
                ("Total Credits", data["data"]["total_credits"]),
                ("Total Debits", data["data"]["total_debits"]),
                ("Net Flow", data["data"]["net_flow"]),
                ("Average Balance", data["data"]["avg_balance"])
            ]
            
            table.setRowCount(len(metrics))
            for i, (metric, value) in enumerate(metrics):
                table.setItem(i, 0, QTableWidgetItem(metric))
                table.setItem(i, 1, QTableWidgetItem(str(value)))
            
            layout.addWidget(table)
        
        widget.setLayout(layout)
        return widget 