from fastapi import FastAPI
import pandas as pd
import ast

app = FastAPI()

@app.get("/")
def index():
    return {"mensaje":"Hola, Jose"}

df = pd.read_csv("df_final.csv")
df_peliculas = pd.read_csv("peliculas.csv")

@app.get("/cantidad_filmaciones_mes/{mes_str}")
def cantidad_filmaciones_mes(mes_str):
    meses_dict = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    # Verificamos si el mes ingresado está en el diccionario
    if mes_str.lower() not in meses_dict:
        raise ValueError(f"El mes '{mes_str}' no es válido.")
    
    # Obtenemos el número del mes
    mes_num = meses_dict[mes_str.lower()]
    # Convertimos la columna en formato de fecha, si no está ya convertida
    df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
    # Contamos cuántas veces aparece el mes
    conteo = df[df["release_date"].dt.month == mes_num].shape[0]
    
    return {"message": f"Se estrenaron {conteo} peliculas en {mes_str}"}

@app.get("/cantidad_filmaciones_dia/{dia_str}")
def cantidad_filmaciones_dia(dia_str):
    dias_dict = {
        'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3, 
        'viernes': 4, 'sabado': 5, 'domingo': 6
    }
    if dia_str.lower() not in dias_dict:
        raise ValueError(f"El día '{dia_str}' no es válido.")
    
    # Obtenemos el número correspondiente al día
    dia_num = dias_dict[dia_str.lower()]
    # Convertimos la columna en formato de fecha, si no está ya convertida
    df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
    # Contamos cuántas veces aparece el día de la semana
    conteo = df[df["release_date"].dt.weekday == dia_num].shape[0]
    
    return {"message": f"Se estrenaron {conteo} peliculas en los dias {dia_str}"}

@app.get("/score_titulo/{titulo_str}")
def score_titulo(titulo_str):
    # Filtramos el dataframe para obtener la fila correspondiente al título
    film = df[df['title'].str.lower() == titulo_str.lower()]
    
    # Verificamos si el título existe
    if film.empty:
        return f"La película '{titulo_str}' no se encontró en el dataset."
    
    # Extraemos el título, año de estreno y score
    titulo = film['title'].values[0]
    anio_estreno = film['release_year'].values[0]
    score = film['popularity'].values[0]
    
    # Retornamos el mensaje formateado
    return f"La película '{titulo}' fue estrenada en el año {anio_estreno} con un score/popularidad de {score}."
 
@app.get("/votos_titulo/{titulo_str}")
def votos_titulo(titulo_str):
    # Filtramos el dataframe para obtener la fila correspondiente al título
    film = df[df['title'].str.lower() == titulo_str.lower()]  
    # Verificamos si el título existe
    if film.empty:
        return f"La película '{titulo_str}' no se encontró en el dataset."
    
    # Obtenemos la cantidad de votos y el promedio de votaciones
    votos = film['vote_count'].values[0]
    promedio_votos = film['vote_average'].values[0]
    anio_estreno = film['release_year'].values[0]
    
    # Verificamos si cumple con el mínimo de 2000 valoraciones
    if votos < 2000:
        return f"La película '{titulo_str}' no cumple con el mínimo de 2000 valoraciones."
    # Retornamos el mensaje formateado
    return f"La película '{titulo_str}' fue estrenada dn el año {anio_estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}."

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor):
    # Filtrar el DataFrame para incluir solo las filas donde el actor está en el cast
    # Convertir la columna 'cast' de string a lista para hacer la búsqueda más sencilla
    df_peliculas['crew'] = df_peliculas['crew'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # Filtrar las películas en las que participó el actor
    actor_movies = df_peliculas[df_peliculas['cast'].apply(lambda x: nombre_actor in x)]
    
    # Calcular el número de películas, el retorno total y el promedio de retorno
    num_movies = actor_movies.shape[0]
    total_return = actor_movies['return'].sum() if num_movies > 0 else 0
    average_return = total_return / num_movies if num_movies > 0 else 0
    
    # Devolver el resultado
    if num_movies > 0:
        return (f"El actor {nombre_actor} ha participado de {num_movies} filmaciones, "
                f"el mismo ha conseguido un retorno de {total_return:.6f} "
                f"con un promedio de {average_return:.6f} por filmación.")
    else:
        return f"El actor {nombre_actor} no ha participado en ninguna filmación."
    return

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director):
    # Convertir la columna 'crew' de string a lista de nombres
    df_peliculas['crew'] = df_peliculas['crew'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
    )
    
    # Verificar si la conversión a listas fue exitosa
    print(df_peliculas['crew'].head())  # Debug: ver las primeras filas de 'crew' para asegurarse que son listas

    # Filtrar las películas dirigidas por el director
    director_movies = df_peliculas[df_peliculas['crew'].apply(lambda x: nombre_director in x)]

    # Verificar si hay películas del director
    if director_movies.empty:
        return {"mensaje": f"El director {nombre_director} no ha dirigido ninguna película."}

    # Calcular el retorno total
    total_return = director_movies['return'].sum()

    # Preparar la salida de las películas
    movies_info = []
    for _, row in director_movies.iterrows():
        movie_info = {
            "titulo": row['title'],
            "fecha_lanzamiento": row['release_date'],
            "retorno": row['return'],
            "costo": row['budget'],
            "ganancia": row['return'] - row['budget']
        }
        movies_info.append(movie_info)

    # Formar la respuesta final
    return {
        "mensaje": f"El director {nombre_director} ha conseguido un retorno total de {total_return:.6f}.",
        "detalles_peliculas": movies_info
    }


