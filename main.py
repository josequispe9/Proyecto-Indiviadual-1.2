from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def index():
    return {"mensaje":"Hola, Jose"}

df = pd.read_csv("df_final.csv")

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

