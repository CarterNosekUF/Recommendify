from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from textblob import TextBlob

audioCols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 
             'instrumentalness', 'liveness', 'valence', 'tempo']


def one_hot_encode(df, name, col):
  if df is None or df.empty or col not in df.columns:
        print(f"Invalid DataFrame or column: {df}, {col}")
        return pd.DataFrame()

  encoded_df = pd.get_dummies(df[col])
  audio_feature_names = encoded_df.columns
  encoded_df.columns = [name + "|" + str(i) for i in audio_feature_names]
  encoded_df.reset_index(drop=True, inplace=True)
  return encoded_df


def select_columns(df):
  # Returns useful columns
  return df[['track_id', 'popularity','track_name', 'genre','danceability', 
             'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 
             'liveness', 'valence', 'tempo']]


def get_opinion(text):
  blob = TextBlob(text).sentiment
  return blob.subjectivity # type: ignore


def get_polarization(text):
  return TextBlob(text).sentiment.polarity # type: ignore


def get_magnitude(score, type):
  if type == 'polarization':
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'
  else:
    if score < 1/3:
      return 'low'
    elif score > 1/3:
      return 'high'
    else:
      return 'medium'


def mood_analysis(df, col):
  df['opinion'] = df[col].apply(get_opinion).apply(lambda x : get_magnitude(x, 'opinion'))
  df['polarization'] = df[col].apply(get_polarization).apply(lambda x: get_magnitude(x, 'polarization'))
  return df


def get_total_features(df: pd.DataFrame, colsToScale: list) -> pd.DataFrame:
  features = []

  df = mood_analysis(df, 'track_name')

  features.append(one_hot_encode(df, 'opinion', 'opinion') * 0.3)
  features.append(one_hot_encode(df, 'polarization', 'polarization') * 0.5)
  features.append(one_hot_encode(df, 'key', 'key') * 0.5)
  features.append(one_hot_encode(df, 'mode', 'key') * 0.5)
  features.append(one_hot_encode(df, 'genre', 'genre'))

  popularity = df[['popularity']].reset_index(drop=True)
  scaler = MinMaxScaler()
  features.append(pd.DataFrame(scaler.fit_transform(popularity), columns = popularity.columns) * 0.2)

  cols = df[colsToScale].reset_index(drop=True)
  features.append(pd.DataFrame(scaler.fit_transform(cols), columns = cols.columns) * 0.2)

  totalFeatures = pd.concat(features, axis=1)
  totalFeatures['track_id'] = df['track_id'].values

  return totalFeatures

def playlist_vectorizer(allFeatures: pd.DataFrame, normalizedPlaylist: pd.DataFrame):
  normalizedPlaylist = normalizedPlaylist.reindex(columns=normalizedPlaylist.columns.union(
    allFeatures.columns, sort=False), fill_value=0)
  # Gets every song (with accompanying features) not included in the given playlist
  otherFeatures = allFeatures[~allFeatures['track_id'].isin(normalizedPlaylist['track_id'].values)]
  playlistNoID = normalizedPlaylist.drop(columns='track_id')
  otherFeatures = otherFeatures.reindex(columns=otherFeatures.columns.union(normalizedPlaylist.columns, sort=False), fill_value=0)


  return (playlistNoID.sum(axis=0), otherFeatures)

def get_similarities(dataset: pd.DataFrame, playlistVector, otherFeatures: pd.DataFrame):
  dataset_exclusive = dataset[dataset['track_id'].isin(otherFeatures['track_id'].values)]
  something = playlistVector.values.reshape(1, -1)
  print(otherFeatures.drop('track_id', axis=1).values.shape)
  print(something.shape)
  dataset_exclusive['similarity'] = cosine_similarity(otherFeatures.drop('track_id', axis=1).values
                                                      , something)[:,0]
  top_10_tracks = dataset_exclusive.sort_values('similarity',ascending = False).head(10)
  return top_10_tracks

def generate_similarity_matrix(datasetFilePath: str, playlistArr) -> pd.DataFrame:
  playlistDF = pd.DataFrame(playlistArr)
  dfDataset = pd.read_csv(datasetFilePath)
  # dfDataset = dfDataset.head(100000)
  dfDataset = select_columns(dfDataset)
  dfDataset = dfDataset.dropna(subset=['track_name'])
  datasetFeatures = get_total_features(dfDataset, audioCols)

  playlistDF = select_columns(playlistDF)
  playlistDF = playlistDF.dropna(subset='track_name')
  playlistFeatures = get_total_features(playlistDF, audioCols)

  normalizedPlaylist, otherFeatures = playlist_vectorizer(datasetFeatures, playlistFeatures)

  simMatrix = get_similarities(dfDataset, normalizedPlaylist, otherFeatures)

  return simMatrix


