# Recomendador
## Archivos
- recomendador.py: Archivo de python que contiene el código que va a encargarse de encontrar las películas o series más relacionadas
- requirements.txt: fichero de texto que contiene las librerías necesarias para ejecutar el script de python
- netflix_titles.csv: fichero csv que contiene los datos con los que vamos a trabajar

## Descripción del script
Para poder obtener las recomendaciones se ha elaborado un programa que sigue una estructura ETL, en la cual la función "transform" es la encargada de llevar a cabo una filtración de los datos poco a poco, hasta finalmente obtener el resultado final. Para llevar a cabo esta filtración, primero nos quedamos solo con películas si el usuario ha introducido una película, o con una serie de televisión si introduce una serie. Luego, calculamos la distancia relativa con cada película del DataFrame. Para ello, hemos establecido unos pesos que reflejan la importancia de cada atributo de las películas, siendo el orden de mayor a menor importancia géneros, director y, por último, actores. En base a eso, cuanto mayor sea la distancia, más próxima a la película se encuentra, por lo que ordenamos el DataFrame de mayor a menor distancia y nos quedamos con los tres primeros elementos.
Luego en la función "load" se lleva a cabo la impresión por pantalla de las 3 películas o series de televisión
