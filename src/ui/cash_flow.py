from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,QToolButton, QStackedWidget, QLabel, QComboBox, QSlider,QDoubleSpinBox,QSizePolicy, QApplication
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import sys
from matplotlib.patches import ArrowStyle

class CustomNavigationToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        
        # Define the style for all toolbar buttons
        button_style = """
            QToolButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
                margin: 1px;
            }
            QToolButton:hover {
                background-color: #34495E;
            }
            QToolButton:pressed {
                background-color: #1ABC9C;
            }
            QToolButton:checked {
                background-color: #16A085;
            }
            QToolButton:disabled {
                background-color: #95A5A6;
            }
        """
        
        # Apply the style to all buttons in the toolbar
        for button in self.findChildren(QPushButton) + self.findChildren(QToolButton):
            button.setStyleSheet(button_style)
        
        # Set size policy for the toolbar
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


# dummy_data_for_network_graph = pd.DataFrame([
#         {'Value Date': '01-04-2022', 'Description': 'openingbalance', 'Debit': 0.00, 'Credit': 3397.13, 'Balance': 3397.13, 'Category': 'Opening Balance'},
#         {'Value Date': '01-04-2022', 'Description': 'mbrentref209108561454', 'Debit': 3000.00, 'Credit': 0.00, 'Balance': 397.13, 'Category': 'Rent Paid'},
#         {'Value Date': '01-04-2022', 'Description': 'upi/saisuvidhasho/209125626472/paymentfromph', 'Debit': 140.00, 'Credit': 0.00, 'Balance': 257.13, 'Category': 'UPI-Dr'},
#         {'Value Date': '01-04-2022', 'Description': 'mbsenttogane62491633408impsref209121360374', 'Debit': 200.00, 'Credit': 0.00, 'Balance': 57.13, 'Category': 'Creditor'},
#         {'Value Date': '01-04-2022', 'Description': 'rev:imps62491633408ref209121360374', 'Debit': 0.00, 'Credit': 200.00, 'Balance': 257.13, 'Category': 'Refund/Reversal'},
#         {'Value Date': '03-04-2022', 'Description': 'recd:imps/209310634191/mrsmeena/kkbk/x8247/ineti', 'Debit': 0.00, 'Credit': 3000.00, 'Balance': 3057.13, 'Category': 'Debtor'},
#         {'Value Date': '03-04-2022', 'Description': 'upi/kfcsapphirefo/209376260786/ye', 'Debit': 250.00, 'Credit': 0.00, 'Balance': 807.13, 'Category': 'Food Expense/Hotel'},
#         {'Value Date': '04-04-2022', 'Description': 'ib:receivedfromruteshslodaya06580010004867', 'Debit': 0.00, 'Credit': 18269.00, 'Balance': 18516.13, 'Category': 'Suspense'},
#         {'Value Date': '05-04-2022', 'Description': 'mbloanref209507057778', 'Debit': 6000.00, 'Credit': 0.00, 'Balance': 7316.13, 'Category': 'Loan given'},
#         {'Value Date': '07-04-2022', 'Description': 'upi/irctcwebupi/209730050986/oid100003321095', 'Debit': 2568.60, 'Credit': 0.00, 'Balance': 3387.03, 'Category': 'Travelling Expense'},
#     ])
# data = pd.DataFrame([
#         {'Value Date': '01-04-2022', 'Description': 'openingbalance', 'Debit': 0.00, 'Credit': 3397.13, 'Balance': 3397.13, 'Category': 'A'},
#         {'Value Date': '01-04-2022', 'Description': 'mbrentref209108561454', 'Debit': 3000.00, 'Credit': 0.00, 'Balance': 397.13, 'Category': 'B'},
#         {'Value Date': '01-04-2022', 'Description': 'upi/saisuvidhasho/209125626472/paymentfromph', 'Debit': 140.00, 'Credit': 0.00, 'Balance': 257.13, 'Category': 'C'},
#         {'Value Date': '01-04-2022', 'Description': 'mbsenttogane62491633408impsref209121360374', 'Debit': 200.00, 'Credit': 0.00, 'Balance': 57.13, 'Category': 'A'},
#         {'Value Date': '01-04-2022', 'Description': 'rev:imps62491633408ref209121360374', 'Debit': 0.00, 'Credit': 200.00, 'Balance': 257.13, 'Category': 'B'},
#         {'Value Date': '03-04-2022', 'Description': 'recd:imps/209310634191/mrsmeena/kkbk/x8247/ineti', 'Debit': 0.00, 'Credit': 3000.00, 'Balance': 3057.13, 'Category': 'C'},
#         {'Value Date': '03-04-2022', 'Description': 'upi/kfcsapphirefo/209376260786/ye', 'Debit': 250.00, 'Credit': 0.00, 'Balance': 807.13, 'Category': 'A'},
#         {'Value Date': '04-04-2022', 'Description': 'ib:receivedfromruteshslodaya06580010004867', 'Debit': 0.00, 'Credit': 18269.00, 'Balance': 18516.13, 'Category': 'B'},
#         {'Value Date': '05-04-2022', 'Description': 'mbloanref209507057778', 'Debit': 6000.00, 'Credit': 0.00, 'Balance': 7316.13, 'Category': 'C'},
#         {'Value Date': '07-04-2022', 'Description': 'upi/irctcwebupi/209730050986/oid100003321095', 'Debit': 2568.60, 'Credit': 0.00, 'Balance': 3387.03, 'Category': 'D'},
#     ])

class CashFlowNetwork(QMainWindow):
    def __init__(self,data,CA_id=None):
        super().__init__()
        self.setGeometry(100, 100, 1200, 900)
        self.data = data
        
        # Enhanced stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QWidget {
                background-color: #f0f0f0;
                color: #333333;
            }
            QLabel {
                color: #333333;
                font-weight: bold;
            }
            QPushButton, QComboBox {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px;
                min-width: 80px;
            }
            QPushButton:hover, QComboBox:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #1ABC9C;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid none;
                border-right: 5px solid none;
                border-top: 5px solid white;
                width: 0;
                height: 0;
                margin-right: 5px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #ffffff;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2C3E50;
                border: none;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #34495E;
            }
        """)
        
        # Create main widget and layout
        main_widget = QWidget()
        main_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add some padding around the edges
        main_layout.setSpacing(10)  # Space between widgets
        
        # Create controls container
        controls_widget = QWidget()
        controls_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
       
       
        # Create figure and canvas
        self.figure = plt.figure(figsize=(12, 10))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create custom navigation toolbar
        nav_toolbar = CustomNavigationToolbar(self.canvas, self)
   
        
        # Node size slider
        size_label = QLabel("Node Size:")
        self.node_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.node_size_slider.setRange(500, 5000)
        self.node_size_slider.setValue(2000)
        self.node_size_slider.valueChanged.connect(self.update_graph)
  
        controls_layout.addWidget(size_label)
        controls_layout.addWidget(self.node_size_slider)
        # controls_layout.addStretch()
        
        
        
        # Create a container for the graph
        graph_container = QWidget()
        graph_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(0)
        
        # Add canvas to graph container
        graph_layout.addWidget(self.canvas)
        
        # Add all widgets to main layout
        main_layout.addWidget(controls_widget)
        main_layout.addWidget(nav_toolbar)
        main_layout.addWidget(graph_container)
        
        self.setCentralWidget(main_widget)
        
        # Professional color palette
        self.color_palette = {
            # 'Rent Paid': '#E74C3C',
            # 'UPI-Dr': '#3498DB',
            # 'Creditor': '#9B59B6',
            # 'Refund/Reversal': '#27AE60',
            # 'Debtor': '#F1C40F',
            # 'Food Expense/Hotel': '#E67E22',
            # 'Suspense': '#95A5A6',
            # 'Loan given': '#D35400',
            # 'Travelling Expense': '#16A085'
            'Person': '#F1C40F',  # Red for person
            'Entity': '#3498DB'   # Blue for entities
        }
        
        self.k_value = QDoubleSpinBox()
        self.k_value.setValue(50)
        
        # Enable the window to be resized
        self.setMinimumSize(800, 600)
        
        self.create_graph()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_graph()  # Redraw the graph when window is resized

    def create_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        G = nx.DiGraph()

        node_sizes = {}
        edge_weights = {}

        # Get unique names and their sizes/colors
        unique_names = self.data['Name'].unique()
        name_sizes = {name: self.node_size_slider.value() * 1.5 for name in unique_names}
        name_colors = {name: self.color_palette['Person'] for name in unique_names}

        # Process each transaction
        for _, row in self.data.iterrows():
            name = row['Name']
            entity = row['Entity']

            # Add nodes if they don't exist
            if name not in G:
                G.add_node(name, type='Person', size=name_sizes.get(name, self.node_size_slider.value()), color=name_colors.get(name, self.color_palette['Person']))
            if entity not in G:
                G.add_node(entity, type='Entity', size=self.node_size_slider.value(), color=self.color_palette['Entity'])

            # Add edges based on debit/credit
            if not pd.isna(row['Debit']):
                G.add_edge(name, entity, amount=-row['Debit'], weight=row['Debit'], transaction_type='debit')
                edge_weights[(name, entity)] = row['Debit']
                node_sizes[name] = node_sizes.get(name, 0) + row['Debit']
                node_sizes[entity] = node_sizes.get(entity, 0) + row['Debit']
            if not pd.isna(row['Credit']):
                G.add_edge(entity, name, amount=row['Credit'], weight=row['Credit'], transaction_type='credit')
                edge_weights[(entity, name)] = row['Credit']
                node_sizes[name] = node_sizes.get(name, 0) + row['Credit']
                node_sizes[entity] = node_sizes.get(entity, 0) + row['Credit']

        base_size = self.node_size_slider.value()

        if node_sizes:
            max_size = max(node_sizes.values())
            node_sizes = {k: (base_size/2) + (v / max_size) * base_size for k, v in node_sizes.items()}

        pos = nx.spring_layout(G, k=self.k_value.value())
        
        # Calculate node radii for arrow adjustments
        node_radii = {}
        for node in G.nodes():
            node_type = G.nodes[node]['type']
            size = G.nodes[node]['size'] if node_type == 'Person' else node_sizes.get(node, base_size)
            # Convert node size to radius in points
            radius = (size / plt.rcParams['figure.dpi']) ** 0.5 * 20
            node_radii[node] = radius
        
        # Draw nodes
        for node, (x, y) in pos.items():
            node_type = G.nodes[node]['type']
            color = G.nodes[node]['color'] if node_type == 'Person' else self.color_palette[node_type]
            size = G.nodes[node]['size'] if node_type == 'Person' else node_sizes.get(node, base_size)
            node_collection = nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=[color], node_size=size, alpha=0.85, ax=ax)
            node_collection.set_zorder(10 if node_type == 'Person' else 1)
        
         # Custom arrow style with a smaller head
        arrow_style = ArrowStyle("->", head_length=10, head_width=8)

        # # Draw edges with different colors based on transaction type
        # for (u, v, d) in G.edges(data=True):
        #     edge_color = 'red' if d.get('transaction_type') == 'debit' else 'green'
        #     alpha = 0.6
        #     edge = nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=edge_color, alpha=alpha, ax=ax, connectionstyle="arc3,rad=0.1", arrowsize=20)
        #     if isinstance(edge, list):
        #         for e in edge:
        #             e.set_zorder(3)
        #     else:
        #         edge.set_zorder(3)
# Draw edges with adjusted connection points

        for (u, v, d) in G.edges(data=True):
            edge_color = 'red' if d.get('transaction_type') == 'debit' else 'green'
            
            # Get start and end positions
            start_pos = pos[u]
            end_pos = pos[v]
            
            # Calculate the direction vector
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            dist = (dx**2 + dy**2)**0.5
            
            # Normalize the direction vector
            dx, dy = dx/dist, dy/dist
            
            # Adjust start and end points by node radii
            start_radius = node_radii[u] / 1000  # Convert to graph coordinates
            end_radius = node_radii[v] / 1000    # Convert to graph coordinates
            
            # Move start and end points to node borders
            new_start = (start_pos[0] + dx * start_radius, 
                        start_pos[1] + dy * start_radius)
            new_end = (end_pos[0] - dx * end_radius,
                      end_pos[1] - dy * end_radius)
            
            # Draw the edge with adjusted positions
            ax.annotate("", xy=new_end, xytext=new_start,
                       arrowprops=dict(arrowstyle=arrow_style, color=edge_color, 
                                     alpha=0.6, connectionstyle="arc3,rad=0.1"))
        
        # Add labels
        labels = nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_family='sans-serif', alpha=0.75, ax=ax)
        for label in labels.values():
            label.set_zorder(3)

        # Add edge labels with amounts
        edge_labels = nx.get_edge_attributes(G, 'amount')
        edge_labels = {k: f'₹{abs(v):,.2f}' for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8, font_family='sans-serif')

        ax.axis('off')
        self.canvas.draw()

    def update_graph(self):
        self.create_graph()


# if __name__ == "__main__":
#     dummy_data_for_network_graph = pd.DataFrame([
#         {'Value Date': '01-04-2022', 'Description': 'openingbalance', 'Debit': 0.00, 'Credit': 3397.13, 'Balance': 3397.13, 'Category': 'Opening Balance'},
#         {'Value Date': '01-04-2022', 'Description': 'mbrentref209108561454', 'Debit': 3000.00, 'Credit': 0.00, 'Balance': 397.13, 'Category': 'Rent Paid'},
#         {'Value Date': '01-04-2022', 'Description': 'upi/saisuvidhasho/209125626472/paymentfromph', 'Debit': 140.00, 'Credit': 0.00, 'Balance': 257.13, 'Category': 'UPI-Dr'},
#         {'Value Date': '01-04-2022', 'Description': 'mbsenttogane62491633408impsref209121360374', 'Debit': 200.00, 'Credit': 0.00, 'Balance': 57.13, 'Category': 'Creditor'},
#         {'Value Date': '01-04-2022', 'Description': 'rev:imps62491633408ref209121360374', 'Debit': 0.00, 'Credit': 200.00, 'Balance': 257.13, 'Category': 'Refund/Reversal'},
#         {'Value Date': '03-04-2022', 'Description': 'recd:imps/209310634191/mrsmeena/kkbk/x8247/ineti', 'Debit': 0.00, 'Credit': 3000.00, 'Balance': 3057.13, 'Category': 'Debtor'},
#         {'Value Date': '03-04-2022', 'Description': 'upi/kfcsapphirefo/209376260786/ye', 'Debit': 250.00, 'Credit': 0.00, 'Balance': 807.13, 'Category': 'Food Expense/Hotel'},
#         {'Value Date': '04-04-2022', 'Description': 'ib:receivedfromruteshslodaya06580010004867', 'Debit': 0.00, 'Credit': 18269.00, 'Balance': 18516.13, 'Category': 'Suspense'},
#         {'Value Date': '05-04-2022', 'Description': 'mbloanref209507057778', 'Debit': 6000.00, 'Credit': 0.00, 'Balance': 7316.13, 'Category': 'Loan given'},
#         {'Value Date': '07-04-2022', 'Description': 'upi/irctcwebupi/209730050986/oid100003321095', 'Debit': 2568.60, 'Credit': 0.00, 'Balance': 3387.03, 'Category': 'Travelling Expense'},
#     ])

#     dummy_data = pd.DataFrame([
#     {'Name': 'Poojan Vig', 'Debit': float('nan'), 'Credit': 426.0, 'Entity': 'barb0chembu'},
#     {'Name': 'Poojan Vig', 'Debit': 144.0, 'Credit': float('nan'), 'Entity': 'hdfc0000001'},
#     {'Name': 'Poojan Vig', 'Debit': 3000.0, 'Credit': float('nan'), 'Entity': 'vigpoojanmanish'},
#     {'Name': 'Poojan Vig', 'Debit': float('nan'), 'Credit': 150.0, 'Entity': 'jsbl0000018'},
#     {'Name': 'Poojan Vig', 'Debit': 15.0, 'Credit': float('nan'), 'Entity': 'sampathvamanshetti'}])
#     df  = pd.read_excel("src/data/network_process_df.xlsx")
#     filtered_df = df[['Name', "Value Date",'Debit', 'Credit', 'Entity']].dropna(subset=['Entity'])
#     print(filtered_df.head())
#     app = QApplication(sys.argv)
#     main_window = CashFlowNetwork(data=filtered_df)
#     main_window.show()
#     sys.exit(app.exec())