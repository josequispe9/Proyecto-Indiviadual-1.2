
## Descripción
Este proyecto tiene como objetivo analizar datos de películas para crear un sistema de recomendación de películas. Utilizando técnicas de ciencia de datos, el sistema sugiere opciones personalizadas para ayudar a los usuarios a descubrir nuevas películas basadas en sus preferencias.

## Tabla de Contenido
- [Descripción](#descripción)
- [Instalación y Requisitos](#instalación-y-requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso y Ejecución](#uso-y-ejecución)
- [Metodología](#metodología)
- [Resultados y Conclusiones](#resultados-y-conclusiones)
- [Contribución y Colaboración](#contribución-y-colaboración)
- [Licencia](#licencia)
- [Autores](#autores)

## Instalación y Requisitos

### Requisitos:
- Python 3.7 o superior
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- pyarrow

## Pasos de instalación:

Clonar el repositorio: git clone https://github.com/josequispe9/Proyecto-Indiviadual-1.2.git
Crear un entorno virtual: python -m venv venv
Activar el entorno virtual:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
Instalar las dependencias: pip install -r requirements.txt

## Estructura del Proyecto
EDA: Jupyter notebooks con el análsis para los datos de entrenamiento del modelo
ETL: Jupyter notebooks con la limpieza realizada a los datasets originales
df_final: Dataset obtenido a partir del ETL
main: Código fuente con las funciones y la API
merge: Jupyter notebooks con la union de los datasets df_final y credits
peliculas: Dataset obtenido a partir del merge
peliculas_para_el_modelo2: Dataset obtenido a partir del EDA
README.md: Documentación.


## Uso y Ejecución
Ejecutar ETL.ipynb para análisis y limpieza del dataset de peliculas y obtener 'df_final.parquet'
Ejecutar merge.ipynb para unir los dataset 'df_final.parquet' y 'credits' obteniendo el dataset 'peliculas'
Ejecutar EDA.ipynb para realizar la exploracion y reducir el tamaño del dataset que usara el modelo


Metodología
Se aplicaron modelos de similitud del coseno.

Resultados y Conclusiones
El sistema de recomendación sugiere películas de acuerdo a las preferencias del usuario, mejorando la experiencia de descubrimiento de contenido.
La version gratis en Render trabaja en un entorno con muy poca memoria


Autores
Jose Quispe.