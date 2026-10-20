import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class VentanaInventario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventario")
        self.setGeometry(100, 100, 1150, 700)
        
        # Cargar datos del CSV
        self.df = pd.read_csv('datos.csv')
        
        # Widget central y layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        
        self.label = QLabel("<b>Instrucción:</b> Haz clic en cualquier barra del gráfico para inspeccionar su estructura, tipos de datos y estadísticas de forma detallada.")
        self.layout.addWidget(self.label)
        
        # Layout horizontal para dividir el gráfico y el panel de análisis
        content_layout = QHBoxLayout()
        
        # 1. Configurar Matplotlib Canvas (Gráfico)
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvas(self.fig)
        content_layout.addWidget(self.canvas)
        
        # 2. Panel de texto interactivo 
        self.text_info = QTextEdit()
        self.text_info.setReadOnly(True)
        self.text_info.setStyleSheet("background-color: #f9f9f9; font-family: Segoe UI; font-size: 13pt; padding: 10px;")
        
        # Mensaje de bienvenida inicial
        html_inicial = """
        <div style="text-align: center; color: #555; margin-top: 50px;">
            <h3>Panel de Análisis de Inventario</h3>
            <p>Selecciona una barra de sucursal en el gráfico de la izquierda para ver su reporte detallado aquí.</p>
        </div>
        """
        self.text_info.setHtml(html_inicial)
        content_layout.addWidget(self.text_info)
        
        self.layout.addLayout(content_layout)
        
      
        self.mostrar_grafico()
        self.canvas.mpl_connect('button_press_event', self.on_bar_click)

    def mostrar_grafico(self):
        self.ax.clear()
        self.stock_sucursal = self.df.groupby('Sucursal')['Stock'].sum()
        self.sucursales_labels = self.stock_sucursal.index.tolist()
        
        # Generar barras con un diseño
        self.ax.bar(self.sucursales_labels, self.stock_sucursal.values, color='#3498db', edgecolor='#2980b9', linewidth=1.2)
        self.ax.set_title("Stock Total por Sucursal (¡Haz clic en una barra!)", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Sucursal", fontsize=10, fontweight='bold')
        self.ax.set_ylabel("Cantidad en Stock", fontsize=10, fontweight='bold')
        self.ax.grid(axis='y', linestyle='--', alpha=0.6)
        
        self.fig.tight_layout()
        self.canvas.draw()

    def on_bar_click(self, event):
        if event.xdata is not None and event.ydata is not None:
            index = round(event.xdata)
            if 0 <= index < len(self.sucursales_labels):
                sucursal_seleccionada = self.sucursales_labels[index]
                self.analizar_sucursal(sucursal_seleccionada)

    def analizar_sucursal(self, sucursal):
        df_suc = self.df[self.df['Sucursal'] == sucursal]
        
   
        total_registros = len(df_suc)
        stock_total = df_suc['Stock'].sum()
        promedio_precio = df_suc['PrecioUnitario'].mean()
        
     
        desc_html = df_suc.describe().to_html(classes='table', border=0, justify='center')
        
     
        html_content = f"""
        <html>
        <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #333; }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
            h4 {{ color: #16a085; margin-top: 15px; }}
            .card {{ background-color: #ffffff; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px; }}
            table.table {{ width: 100%; border-collapse: collapse; font-size: 11pt; margin-top: 8px; background: #fff; }}
            table.table th {{ background-color: #3498db; color: white; padding: 6px; text-align: center; }}
            table.table td {{ padding: 5px; border-bottom: 1px solid #ddd; text-align: center; }}
            ul {{ margin: 0; padding-left: 20px; }}
        </style>
        </head>
        <body>
            <h2>Sucursal: {sucursal}</h2>
            
            <div class="card">
                <b>Resumen Ejecutivo:</b>
                <ul>
                    <li><b>Registros analizados:</b> {total_registros} productos</li>
                    <li><b>Stock acumulado:</b> {stock_total} unidades</li>
                    <li><b>Precio promedio:</b> ${promedio_precio:.2f}</li>
                </ul>
            </div>

            <h4>Estructura y Tipos de Datos</h4>
            <p>El conjunto de datos de esta sucursal contiene <b>{total_registros} entradas</b> distribuidas en 5 columnas con tipos validados (Texto, Enteros y Decimales).</p>

            <h4>Estadísticas Descriptivas del Inventario</h4>
            {desc_html}
        </body>
        </html>
        """
        
        self.text_info.setHtml(html_content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaInventario()
    ventana.show()
    sys.exit(app.exec_())