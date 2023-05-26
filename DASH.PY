from flask import Flask, render_template
import csv
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    graph_data = []

    population_pyramid_data = generate_population_pyramid('Comisiones_limpio.csv')
    graph_data.append(population_pyramid_data)

    top_values_data = generate_top_values('Siniestros_limpio.csv', 'CAUSA DEL SINIESTRO', 'Causa del siniestro Top 15')
    graph_data.append(top_values_data)

    cobertura_data = generate_cobertura_pie_chart('Emisiones_limpio.csv', 'COBERTURA', 'Cobertura')
    graph_data.append(cobertura_data)

    state_distribution_data = generate_state_distribution('Ors_Entidad Limp_FINAL-2.csv', 'ENTIDAD', 'Distribución por entidad federativa')
    graph_data.append(state_distribution_data)

    return render_template('index.html', graph_data=graph_data)

def generate_population_pyramid(file_path):
    ages_male = []
    ages_female = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            age = int(row['EDAD'])
            sex = row['SEXO']

            if sex == 'Masculino':
                ages_male.append(age)
            elif sex == 'Femenino':
                ages_female.append(age)

    fig, ax = plt.subplots()

    ax.invert_yaxis()

    ax.hist(ages_male, bins=max(ages_male)-min(ages_male)+1, range=(min(ages_male)-0.5, max(ages_male)+0.5),
            alpha=0.7, label='Masculino', orientation='horizontal')
    ax.hist(ages_female, bins=max(ages_female)-min(ages_female)+1, range=(min(ages_female)-0.5, max(ages_female)+0.5),
            alpha=0.7, label='Femenino', orientation='horizontal')

    ax.set_xlabel('Población')
    ax.set_ylabel('Edad')
    ax.set_title('Pirámide de población')

    ax.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode()

    return {
        'graph': graph,
        'title': 'Pirámide de población'
    }

def generate_top_values(file_path, column_name, title):
    df = pd.read_csv(file_path)

    top_values = df[column_name].value_counts().head(15)

    fig, ax = plt.subplots()
    top_values.plot(kind='barh', ax=ax)

    ax.set_xlabel('Cantidad')
    ax.set_ylabel(column_name)
    ax.set_title(title)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode()

    return {
        'graph': graph,
        'title': title
    }

def generate_cobertura_pie_chart(file_path, column_name, title):
    df = pd.read_csv(file_path)

    cobertura_counts = df[column_name].value_counts()

    fig, ax = plt.subplots()
    cobertura_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')

    ax.set_title(title)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode()

    return {
        'graph': graph,
        'title': title
    }

def generate_state_distribution(file_path, column_name, title):
    df = pd.read_csv(file_path)

    state_counts = df[column_name].value_counts()

    fig, ax = plt.subplots()
    state_counts.plot(kind='barh', ax=ax)

    ax.set_xlabel('Cantidad')
    ax.set_ylabel('Estado')
    ax.set_title(title)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode()

    return {
        'graph': graph,
        'title': title
    }

if __name__ == '__main__':
    app.run()
    
