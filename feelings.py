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


def average_feelings(sublist):
    if not sublist:
        return None
    t_score = {
        'anger': 0,
        'contempt': 0,
        'disgust': 0,
        'fear': 0,
        'happiness': 0,
        'neutral': 0,
        'sadness': 0,
        'surprise': 0,
    }
    for item in sublist:
        if 'scores' in item:
            for k, v in item['scores'].items():
                t_score[k] += v
    length = len(sublist)
    f_score = map(lambda (k, v): (k, v / length), t_score.items())
    return dict(f_score)
