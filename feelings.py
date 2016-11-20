def to_music(face):
    if not face:
        return None
    anger = face['anger']
    disgust = face['disgust']
    fear = face['fear']
    contempt = face['contempt']
    happiness = face['happiness']
    neutral = face['neutral']
    sadness = face['sadness']
    surprise = face['surprise']
    return {
        'target_acousticness': neutral,
        'target_danceability': happiness * 5 - disgust - sadness - fear,
        'target_valence': happiness - contempt - anger + surprise,
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
