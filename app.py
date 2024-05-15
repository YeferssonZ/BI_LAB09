import mysql.connector
from flask import Flask, render_template
from sklearn.tree import DecisionTreeClassifier
import numpy as np

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'BIlab09'
}

@app.route('/')
def index():
    # Conexión a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Seleccionar datos de empleados
    cursor.execute("SELECT edad, salario, departamento_id FROM empleados")
    results = cursor.fetchall()

    # Procesamiento de datos para el modelo de árbol de decisiones
    X = np.array([[row[0], row[1]] for row in results])  # Features: edad, salario
    y = np.array([row[2] for row in results])  # Target: departamento_id

    # Entrenamiento del modelo de árbol de decisiones
    clf = DecisionTreeClassifier()
    clf.fit(X, y)

    # Predecir usando el modelo entrenado
    sample_data = np.array([[28, 50000], [45, 62000], [33, 55000], [29, 60000], [35, 58000], [40, 60000], [37, 70000]])
    predictions = clf.predict(sample_data)

    # Convertir las predicciones a un formato entendible
    department_names = {
        1: 'Ventas', 2: 'Marketing', 3: 'IT', 4: 'Recursos Humanos',
        5: 'Finanzas', 6: 'Logística', 7: 'Producción', 8: 'Calidad'
    }
    resultados_arbol = [department_names[pred] for pred in predictions]

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Renderizar la plantilla HTML con los resultados
    return render_template('index.html', resultados=resultados_arbol, sample_data=sample_data, resultados_len=len(resultados_arbol))

if __name__ == '__main__':
    app.run(debug=True)
