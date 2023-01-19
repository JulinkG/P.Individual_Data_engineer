from fastapi import FastAPI
import pandas as pd

#Dotamos a la api de un título, descripción y versión
app = FastAPI(title='Proyecto individual Julián Mena',description='Cohorte de Data 06', version='1.0.0')

#Primera función donde la API va a tomar mi dataframe para las consultas.
@app.get('/')
async def read_root():
    return {'Mi primera API'}
    
@app.on_event('startup')
async def startup():
    global df
    df = pd.read_csv('datos_completos.csv')

#función que cuenta la cantidad de veces que aparece esa palabra en los títulos de la plataforma, prefiero dejar el count cómo una lista por
# si en algún momento se desean ver los títulos bajos los que aparece dicha palabra

@app.get('/get_word_count/({platform}, {word})')
async def get_word_count(platform:str,palabra:str):
        count = []
        agrupado = df[df['platform']==platform]
        for i in agrupado['title']:
            if palabra in i:
                count.append(i)

        return (str(platform),str(len(count)))

#función que te da el conteo de películas según su score y plataforma
@app.get('/get_score_count/({platform},{score},{year})')
async def get_score_count(platform:str,score:int,year:int):
        peliculas = df[df['type']=='movie']
        agrupado = peliculas[peliculas['platform']==platform]
        agrupado2 = agrupado[agrupado['release_year']==year]
        count = agrupado2[agrupado2['score']>score]

        return (str(platform),str(len(count)))

#Función que arroja la segunda película según su score en orden alfabético
@app.get('/get_second_score/({platform})')
async def get_second_score(platform:str):
        peliculas = df[df['type']=='movie']
        sort = peliculas[peliculas['platform']==platform]
        sorteado=sort.sort_values(by=['score','title'], ascending=[False,True])
        resultado = sorteado.iloc[1]

        return (str(resultado['title']),str(resultado['score']))

#Función que arroja la película o serie de mayor duración
@app.get('/get_longest/({platform},{duration_type},{year})')
async def get_longest(platform:str,duration_type:str,year:int):
        sort1 = df[df['platform']==platform] 
        sort2 = sort1[sort1['duration_type']==duration_type]
        sort3 = sort2[sort2['release_year']==year]
        sorteado=sort3.sort_values(by='duration_int', ascending=False)
        resultado = sorteado.iloc[0]
    
        return (str(resultado['title']),str(resultado['duration_int']),str(resultado['duration_type']))

#Función que cuenta la cantidad de películas según el rating
@app.get('/get_rating_count/({rating})')
async def get_rating_count(rating:str):
        count=[]
        for i in df['rating']:
            if i == rating:
                count.append(i)

        return (str(rating),str(len(count)))



