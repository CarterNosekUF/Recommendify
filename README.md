# Getting Started
First, ensure you have installed the dependencies required to run the python program. The dependencies are stored in *requirements.txt*. To do so, install all files to a directory on your computer. Then, open a terminal in that directory and simply use

```python
pip install -r requirements.txt
```

This will ensure you have all dependencies.

# References

Here is the [link](https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks) to the original dataset of Spotify tracks


*Note: We used this dataset to trim down to around 10,000 songs which each contain 15 columns, creating 150,000 datapoints, this method was used because performing the required operations on 1,000,000+ datapoints was not feasible*

##

We also found use in a general pipeline for building a content-based recommendation system [here](https://towardsdatascience.com/part-iii-building-a-song-recommendation-system-with-spotify-cf76b52705e7)
