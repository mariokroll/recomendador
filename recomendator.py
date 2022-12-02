import pandas as pd
import sys
import re


def calculate_distance(genres: list, director: list, actors: list, row_genres: list, row_director: list, row_actors: list) -> int:
    """
    Calculamos la distancia relativa entre la película o serie introducida y otra serie. La distancia representa lo similar o diferente que es
    con la entrada. Cada variable tiene un peso, siendo los géneros los más importantes o los 'más pesados', seguidos por el director y finalmente,
    los actores.
    """
    
    # Creamos los pesos de cada variable
    w_gen = 45
    w_dir = 35
    w_act = 20
    distance = 0

    # Para cada género del show introducido, comprobamos si está en el show que estamos analizando
    w_gen_ind = w_gen / len(genres)
    for g in row_genres:
        if g in genres:
            distance += w_gen_ind

    # Para cada director del show introducido, comprobamos si está en el show que estamos analizando
    w_dir_ind = w_dir / len(director)
    for d in row_director:
        if d in director:
            distance += w_dir_ind

    # Para cada actor del show introducido, comprobamos si está en el show que estamos analizando
    w_act_ind = w_act / len(actors)
    for act in row_actors:
        if act in actors:
            distance += w_act_ind
    return distance


def contains_genre_listed_in(genre: str, row: str) -> bool:
    coinc = re.findall(genre, row)
    return True if len(coinc) > 0 else False


def extract() -> pd.DataFrame:
    """
    Importamos el DataFrame con el que vamos a trabajar
    """
    df = pd.read_csv('netflix_titles.csv')
    return df


def transform(df: pd.DataFrame, movie_unfiltered:str) -> pd.DataFrame:
    """
    En esta función, filtramos el DataFrame para quedarnos con las 3 películas o series más similares a
    la entrada. Para ello, calculamos la distancia entre la entrada y cada película o serie del DataFrame.
    """
    
    # Convertimos a mayúsculas la primera letra de cada palabra
    movie = movie_unfiltered.title()

    df.fillna('', inplace=True)
    # Comprobamos que la película o serie introducida está en el DataFrame, si no está, salimos del programa
    if movie not in df['title'].values:
        print('-------------------------------\n \tMovie not found \n-------------------------------')
        sys.exit(1)
    else:
        tyoeof = df.loc[df['title'] == movie, 'type'].values[0]
        # Filtramos el DataFrame para quedarnos con películas o series
        df_cut = df.loc[(df['type'] == tyoeof)].copy()

        # Obtenemos los datos de la película para calcular la distancia
        idx = df_cut[df_cut['title']==movie].index.values[0]
        genres =  df_cut.loc[idx, 'listed_in'].split(', ')
        director = df_cut.loc[idx, 'director'].split(', ')
        actors = df_cut.loc[idx, 'cast'].split(', ')
        df_cut.drop(index=idx, inplace=True)

        # Calculamos la distancia entre la película introducida y cada película del DataFrame
        df_cut['distance'] = df_cut.apply(lambda row: calculate_distance(genres, director, actors, row['listed_in'].split(', '), row['director'].split(', '), row['cast'].split(', ')), axis=1)
        df_cut.sort_values(by='distance', inplace=True, ascending=False)

        # Devolvemos las 3 películas más similares
        return df_cut.head(3)


def load(df: pd.DataFrame):
    """
    Imprimimos por pantalla las 3 películas o series más similares a la introducida
    """
    print('\n¡Aquí tienes 3 recomendaciones!')
    print('\t1.', df.head(1).title.values[0])
    df2 = df.tail(2)
    print('\t1.', df2.head(1).title.values[0])
    print('\t1. ', df2.tail(1).title.values[0])
    print()


if __name__ == '__main__':
    movie = input('Introduce el nombre de la película o serie de la que quieres obtener una recomendación: ')
    df_new = extract()
    df = transform(df_new, movie)
    load(df)