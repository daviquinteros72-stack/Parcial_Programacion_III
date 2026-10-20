import pandas as pd
import numpy as np

# Semilla para reproducibilidad
np.random.seed(42)

sucursales = ['San Salvador', 'Santa Ana', 'San Miguel', 'La Libertad', 'Sonsonate']
productos = ['Laptop', 'Impresora', 'Teclado', 'Mouse', 'Monitor', 'Tablet', 'Smartphone', 'Auriculares']
categorias = ['Tecnología', 'Oficina', 'Accesorios', 'Movilidad']

n_registros = 100

data = {
    'Sucursal': np.random.choice(sucursales, n_registros),
    'Producto': np.random.choice(productos, n_registros),
    'Categoria': np.random.choice(categorias, n_registros),
    'Stock': np.random.randint(5, 150, n_registros),
    'PrecioUnitario': np.round(np.random.uniform(15.0, 850.0, n_registros), 2)
}

df = pd.DataFrame(data)

# Guardar en CSV
df.to_csv('datos.csv', index=False)
print("Archivo 'datos.csv' generado exitosamente.")