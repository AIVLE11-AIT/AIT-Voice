def speech_rate_ko(duration, syllable_count):    
    if duration > 0:
        speech_rate = syllable_count / duration
    else:
        raise ValueError("측정 불가")
    
    return speech_rate

def speech_rate_en(duration, word_count):
    minutes = duration / 60.0
    wpm = word_count / minutes
    
    return wpm
