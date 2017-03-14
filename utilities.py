def addzeros(chapt_string):
    chapt_number = float(chapt_string)
    if(chapt_number < 10):
        return '00' + chapt_string
    elif (chapt_number > 9 and chapt_number < 100):
        return '0' + chapt_string
    else:
        return chapt_string
