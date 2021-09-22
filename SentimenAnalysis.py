from functions import clean_text
import matplotlib.pyplot as plt
from sentiment_analysis_spanish import sentiment_analysis
sentiment = sentiment_analysis.SentimentAnalysisSpanish()

def SentimentAnalysis(polarity):
  polarity=float(polarity)
  if polarity <= 0.2:
    return "negativo"
  elif polarity > 0.2 and polarity < 0.5:
    return "Neutral"
  else:
    return "positivo"

def mkSentiment_Analysis(data_group, id_str):
    data_group['text'] = data_group['text'].apply(clean_text)
    data_group['polarity'] = data_group['text'].apply(sentiment.sentiment)
    data_group['analysis'] = data_group['polarity'].apply(SentimentAnalysis)

    tb_counts = data_group.analysis.value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(tb_counts.values, labels = tb_counts.index, autopct='%1.1f%%', shadow=False)
    plt.savefig('results/sentiment/'+ id_str + '.jpg')