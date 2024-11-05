from fastapi import FastAPI
import pandas as pd
import pyarrow
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from scipy.sparse import hstack, csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Cargar los datos
df = pd.read_parquet("df_final.parquet")
df_peliculas = pd.read_parquet("peliculas.parquet")

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
def get_director(nombre_director: str):
    # Filtrar las películas en las que aparece el director en la lista de 'crew'
    director_movies = df_peliculas[df_peliculas['crew'].apply(
        lambda crew_list: nombre_director.strip().lower() in [director.strip().lower() for director in crew_list]
    )]

    # Verificar si hay películas del director
    if director_movies.empty:
        return {"mensaje": f"El director {nombre_director} no ha dirigido ninguna película en la base de datos."}

    # Calcular el retorno total para el director
    total_return = director_movies['return'].sum()

    # Preparar la lista de detalles de cada película
    movies_info = [
        {
            "titulo": row['title'],
            "fecha_lanzamiento": row['release_date'],
            "retorno": row['return'],
            "costo": float(row['budget']) if isinstance(row['budget'], (int, float, str)) and row['budget'] else 0.0,
            "ganancia": row['return'] - float(row['budget']) if isinstance(row['budget'], (int, float, str)) and row['budget'] else row['return']
        }
        for _, row in director_movies.iterrows()
    ]

    # Formar la respuesta final
    return {
        "mensaje": f"El director {nombre_director} ha conseguido un retorno total de {total_return:.6f}.",
        "detalles_peliculas": movies_info
    }




# Cargar el DataFrame para el modelo de recomendaciones
df_model = pd.read_parquet("peliculas_para_el_modelo2.parquet")

# Limpiar el DataFrame del modelo: eliminar filas con NaN en 'overview' y 'genres'
df_model = df_model.dropna(subset=['overview', 'genres'])

# Vectorización de `overview` usando TF-IDF
tfidf = TfidfVectorizer(stop_words='english', max_features=500)  # Limitar características
tfidf_matrix = tfidf.fit_transform(df_model['overview'])

# Reducción de dimensionalidad en la matriz TF-IDF
svd = TruncatedSVD(n_components=30)  # Ajusta según sea necesario
tfidf_reduced = svd.fit_transform(tfidf_matrix)

# Vectorización de `genres` usando MultiLabelBinarizer
mlb = MultiLabelBinarizer()
genres_matrix = mlb.fit_transform(df_model['genres'].str.split(', '))

# Normalización de `vote_average` y `release_year`
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(df_model[['vote_average', 'release_year']].astype('float32'))

# Convertir `scaled_features` a una matriz dispersa
scaled_features_sparse = csr_matrix(scaled_features)

# Verificar dimensiones de las matrices
print("TF-IDF shape:", tfidf_reduced.shape)
print("Genres matrix shape:", genres_matrix.shape)
print("Scaled features shape:", scaled_features_sparse.shape)

# Concatenar todas las características en una matriz final
feature_matrix = hstack([tfidf_reduced, genres_matrix, scaled_features_sparse])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(feature_matrix)

@app.get("/get_recomendaciones/{title}")
def get_recommendations(title: str, top_n: int = 5):
    # Busca el índice de la película en el DataFrame
    idx = df_model[df_model['title'].str.lower() == title.lower()].index
    
    # Manejo de caso donde la película no existe
    if idx.empty:
        return {"error": f"No se encontró la película '{title}' en la base de datos."}
    
    idx = idx[0]  # Toma el primer índice encontrado

    # Aquí no es necesario usar toarray(), ya que cosine_sim es un ndarray
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))

    # Ordenar las puntuaciones
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de las películas recomendadas
    sim_indices = [i[0] for i in sim_scores[1:top_n + 1]]

    # Verificar si hay títulos recomendados
    if not sim_indices:
        return {"error": "No hay recomendaciones disponibles."}
    
    # Obtener los títulos recomendados
    recommended_titles = df_model.iloc[sim_indices]['title'].tolist()
    
    return {"recomendaciones": recommended_titles}