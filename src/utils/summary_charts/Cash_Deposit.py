import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pandas as pd

class CashDeposit(QMainWindow):
    def __init__(self, data):
        super().__init__()
        # set window to take up the whole screen

        # Transaction data (this can be replaced with real data as shown in the example dataframe)
        self.data = data
        print(self.data.head())

        # Process data for monthly aggregation
        self.data['Month-Year'] = self.data['Value Date'].dt.to_period('M')
        monthly_deposits = self.data.groupby('Month-Year')['Credit'].sum().reset_index()
        monthly_deposits['Month-Year'] = monthly_deposits['Month-Year'].astype(str)

        # Prepare lists for plotting
        self.dates = self.data['Value Date'].dt.strftime('%Y-%m-%d').tolist()
        self.deposits = self.data['Credit'].tolist()
        self.months = monthly_deposits['Month-Year'].tolist()
        self.monthly_totals = monthly_deposits['Credit'].tolist()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create and configure QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.browser.setFixedHeight(600)

        layout.addWidget(self.browser)
        self.show_charts()

    def show_charts(self):
        html_content = self.create_charts_html(self.dates, self.deposits, self.months, self.monthly_totals)
        self.browser.setHtml(html_content)

    def create_charts_html(self, dates, deposits, months, monthly_totals):
        # Create the HTML content with Plotly.js for Line and Bar Charts
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0; 
                    width: 100%; 
                    height: 100vh; 
                    font-family: Arial, sans-serif; 
                }}
                #lineChart, #barChart {{ 
                    width: 100%; 
                    height: 45vh;  /* Use viewport height */
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <!-- Line Chart for Daily Deposits -->
            <div id="lineChart"></div>
            <script>
                var dates = {json.dumps(dates)};
                var deposits = {json.dumps(deposits)};

                var lineTrace = {{
                    x: dates,
                    y: deposits,
                    mode: 'lines+markers',
                    name: 'Daily Deposits',
                    marker: {{ color: 'blue' }},
                    line: {{ color: 'blue' }}
                }};

                var lineLayout = {{
                    title: 'Daily Cash Deposits Over Time',
                    xaxis: {{ title: 'Date' }},
                    yaxis: {{ title: 'Withdrawal Amount' }},
                    legend: {{ orientation: 'h', y: 1.2 }},
                    margin: {{ t: 40, l: 60, r: 40, b: 60 }},
                    autosize: true
                }};

                var config = {{ responsive: true }};

                Plotly.newPlot('lineChart', [lineTrace], lineLayout, config);
            </script>

            <!-- Bar Chart for Monthly Deposits -->
            <div id="barChart"></div>
            <script>
                var months = {json.dumps(months)};
                var monthlyTotals = {json.dumps(monthly_totals)};

                var barTrace = {{
                    x: months,
                    y: monthlyTotals,
                    type: 'bar',
                    name: 'Monthly Deposits',
                    marker: {{ color: 'orange' }}
                }};

                var barLayout = {{
                    title: 'Total Cash Deposits by Month',
                    xaxis: {{ title: 'Month-Year' }},
                    yaxis: {{ title: 'Total Withdrawal Amount' }},
                    legend: {{ orientation: 'h', y: 1.2 }},
                    margin: {{ t: 40, l: 60, r: 40, b: 60 }},
                    autosize: true
                }};

                Plotly.newPlot('barChart', [barTrace], barLayout, config);

                // Add window resize handler
                window.addEventListener('resize', function() {{
                    Plotly.relayout('lineChart', {{
                        'xaxis.autorange': true,
                        'yaxis.autorange': true
                    }});
                    Plotly.relayout('barChart', {{
                        'xaxis.autorange': true,
                        'yaxis.autorange': true
                    }});
                }});
            </script>
        </body>
        </html>
        """
        return html