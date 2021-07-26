import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from math import log

def count_incidents(incidents_bow_dic, tokens_tweet):
    for word in incidents_bow_dic:
        incidents_bow_dic[word].append(tokens_tweet.count(word))
    return incidents_bow_dic

def ToCSV(dataframe, topic,name = 'archivoCSV'):
    addr ='Graficas/' + topic + '/'+ name + '.csv'
    dataframe.to_csv(addr, sep=';', encoding = 'utf-8') 

def join_tokens(dic_tokens_tweets):
    all_tweets_text = ''
    for id in dic_tokens_tweets:
        for token in dic_tokens_tweets[id]:
            all_tweets_text += token + ' '
    return all_tweets_text



# Paso 1: contar palabras en los all temas
def count_col(dataframe):
    dic = {'count': []}
    words = []
    for col in dataframe:
        values = list(dataframe.loc[:,col])
        dic['count'].append(sum(values))
        words.append(col)
    df = pd.DataFrame(dic, index = words)
    return df


# Paso 2: Hallar la frecuencia de terminos
def tf(dataframe):
    wd = pd.DataFrame()  
    col_list= list(dataframe)
    dataframe[col_list].sum(axis=1)
    wd['Cantidad'] = dataframe[col_list].sum(axis=1)

    df_tf = dataframe.copy()
    for col in df_tf:
        nrow = len(df_tf[col])
        for i in range(0,nrow):
            df_tf.loc[i+1,col] = df_tf.loc[i+1,col] / wd.loc[i+1,'Cantidad']
    return df_tf


# Paso 3: Hallar la frecuencia inversa de documentos
def idf(dataframe):
    ndoc = len(dataframe)
    idf = {'idf_values': []}
    words = []
    for i in dataframe:
        words.append(i)
        l = list (dataframe.loc[:,i])
        c = 0
        for j in l:
            if (j != 0):
                c += 1
        idf['idf_values'].append(round(log(ndoc/c),3))
    df = pd.DataFrame(idf, index=words)
    return df

# Paso 4: Hallar el tf-idf
def tf_idf(df_tf, df_idf):
    df_tf_idf = df_tf.copy()
    for col in df_tf_idf:
        nrow = len(df_tf_idf[col])
        for i in range(0,nrow):
            df_tf_idf.loc[i+1,col] *= df_idf.loc[col,'idf_values']
    return df_tf_idf


#def count_df(data_frame):
#dic = {'1':['pera','platano','fresa'], '2':['perro', 'gato','jirafa'], '3':['dota', 'domination']}
# def plot_bar(df, top = 5):    
#     fig = plt.figure()
#     ax = fig.add_axes([0,0,2,1])
#     ax.bar(x =df.iloc[:top,:].index, height = df.iloc[:top,0].values)
#     plt.show()
