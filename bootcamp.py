from flask import Flask, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

@app.route('/')
def generate_charts():
    # Load dataset
    df = pd.read_csv(r'sales.csv', parse_dates=['Date'])

    # Create folder to save charts
    os.makedirs('static', exist_ok=True)

    # Line Chart – Daily Total Sales
    daily_sales = df.groupby('Date')['Sales'].sum().reset_index()
    plt.figure(figsize=(7,4))
    sns.lineplot(data=daily_sales, x='Date', y='Sales', marker='o')
    plt.title("Daily Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/line_chart.png")
    plt.close()

    # Bar Chart – Sales by Category
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    plt.figure(figsize=(6,4))
    sns.barplot(data=category_sales, x='Category', y='Sales', palette='Set2')
    plt.title("Sales by Category")
    plt.tight_layout()
    plt.savefig("static/bar_chart.png")
    plt.close()

    # Heatmap – Correlation between Sales, Cost, Profit
    plt.figure(figsize=(5,4))
    sns.heatmap(df[['Sales', 'Cost', 'Profit']].corr(), annot=True, cmap='Blues')
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("static/heatmap.png")
    plt.close()

    # Scatter Plot – Sales vs Profit
    plt.figure(figsize=(6,4))
    sns.scatterplot(data=df, x='Sales', y='Profit', hue='Category', palette='Set1')
    plt.title("Sales vs Profit")
    plt.tight_layout()
    plt.savefig("static/scatter_plot.png")
    plt.close()

    # Pie Chart – Sales distribution by Product
    product_sales = df.groupby('Product')['Sales'].sum()
    plt.figure(figsize=(6,6))
    plt.pie(product_sales, labels=product_sales.index, autopct='%1.1f%%', startangle=140)
    plt.title("Sales Distribution by Product")
    plt.tight_layout()
    plt.savefig("static/pie_chart.png")
    plt.close()

    return '''
    <h2>Retail analytics visuals generated successfully.</h2>
    <ul>
        <li><a href="/chart/line_chart">Line Chart</a></li>
        <li><a href="/chart/bar_chart">Bar Chart</a></li>
        <li><a href="/chart/heatmap">Heatmap</a></li>
        <li><a href="/chart/scatter_plot">Scatter Plot</a></li>
        <li><a href="/chart/pie_chart">Pie Chart</a></li>
    </ul>
    '''

@app.route('/chart/<name>')
def get_chart(name):
    return send_file(f"static/{name}.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
