def to_music(anger, disgust, fear, contempt, happiness, neutral, sadness, surprise):
    return {
        'target_acousticness': neutral,
        'target_danceability': happiness * 5 - disgust - sadness - fear,
        'target_valence': happiness - contempt - anger + surprise,
        'max_liveness': 0.3,
        'min_popularity': 40,
        'target_loudness': 4 * anger,
        'target_mode': int(round(happiness - sadness)),
        'target_tempo': 60 + happiness * 60 + surprise * 30 - 20 * sadness,
    }
