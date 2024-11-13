import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QFile, QTextStream

class DebtorsChart(QMainWindow):
    def __init__(self,data):
        super().__init__()
        self.setGeometry(100, 100, 1200, 600)

        # Create a QWebEngineView
        self.browser = QWebEngineView()
        data = data.sort_values(by="Value Date")
        self.data = data
        
        # # Prepare data
        # dates = ["04-03-2024", "15-07-2023", "19-03-2024", "26-02-2024", "19-04-2023"]
        # credits = [79873.00, 100000.00, 18000.00, 50000.00, 5000.00]
        # balances = [1079401.47, 720361.94, -716597.43, 1039334.47, 249575.78]
        # Extract data from the DataFrame
        dates = data["Value Date"].dt.strftime("%d-%m-%Y").tolist()
        credits = data["Credit"].tolist() if "Credit" in data.columns else []
        balances = data["Balance"].tolist()

        # Create the HTML and JavaScript for the chart
        html_content = self.create_html(dates, credits, balances)
        
        # Load the HTML content into the QWebEngineView
        self.browser.setHtml(html_content)
        self.browser.setFixedHeight(600)


        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.create_data_table_debtor(layout)

    def create_html(self, dates, credits, balances):
        # Create the HTML content with Plotly.js
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <div id="chart" style="width: 100%; height: 100%;"></div>
            <script>
                var dates = {json.dumps(dates)};
                var credits = {json.dumps(credits)};
                var balances = {json.dumps(balances)};
                
                var trace1 = {{
                    x: dates,
                    y: credits,
                    name: 'Credit Amount',
                    type: 'bar'
                }};
                
                var trace2 = {{
                    x: dates,
                    y: balances,
                    name: 'Balance',
                    type: 'scatter',
                    mode: 'lines+markers',
                    yaxis: 'y2'
                }};
                
                var data = [trace1, trace2];
                
                var layout = {{
                    xaxis: {{
                        title: 'Date',
                        tickformat: "%d-%m-%Y",
                         tickangle: -45,  // Rotate x-axis labels for better readability
                    }},
                    yaxis: {{
                        title: 'Credit Amount',
                    }},
                    yaxis2: {{
                        title: 'Balance',
                        overlaying: 'y',
                        side: 'right',
                    }},
                    barmode: 'group',
                    legend: {{
                        orientation: 'h',
                        x: 0.5,
                        y: 1.15,
                        xanchor: 'center',
                        yanchor: 'bottom'
                    }},
                    margin: {{
                        b: 100  // Increase bottom margin for space below the x-axis
                    }}
                }};
                
                Plotly.newPlot('chart', data, layout);
            </script>
        </body>
        </html>
        """
        return html

    def create_data_table_debtor(self, layout):
        web_view = QWebEngineView()
        
        # Prepare table data
        table_data = []
        for _, row in self.data.iterrows():
            table_data.append({
                'date': row["Value Date"].strftime("%d-%m-%Y"),
                'description': row["Description"],
                'debit': f"₹{float(row['Debit']):,.2f}",
                'credit': f"₹{float(row['Credit']):,.2f}",
                'balance': f"₹{float(row['Balance']):,.2f}",
                'category': row["Category"]
            })

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Debtors Data</title>
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
                    # font-size: 14px;
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
                    text-align: center;
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
                <div class="table-header">Debtors Data Table</div>
                <table>
                    <thead>
                        <tr>
                            <th>Value Date </span></th>
                            <th class="description-column">Description </span></th>
                            <th>Debit </span></th>
                            <th>Credit </span></th>
                            <th>Balance </span></th>
                            <th>Category </span></th>
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
        web_view.setMinimumHeight(600)  # Set minimum height for the table
        layout.addWidget(web_view)