import os

def get_highscore(file_name):
    text = ''

    if os.path.isfile(file_name):
        with open(file_name, 'r') as text_file:
            text = text_file.read()
    else:
        f = open(file_name, 'w')
        text = 'high:0,mid:0,low:0,lowest:0,lowestest:0'
        f.write(text)
        f.close()

    text_list = text.split(',')

    to_return = {}

    for element in text_list:
        i = element.split(':')
        to_return[i[0]] = [i[1]]

    return to_return


def write_highscore(file_name, score):
    f = open(file_name, 'w')
    to_write = ''
    for name in ('high','mid','low','lowest', 'lowestest'):
        to_write += name
        to_write += ':'
        to_write += str(score.get(name)[0])
        to_write += ','

    print(to_write)
    to_write = to_write.rstrip(to_write[-1])
    f.write(to_write)
    f.close()


def set_highscore(file_name, score):
    scores = get_highscore(file_name)

    old_highscore = scores.get('high')[0]
    old_midscore = scores.get('mid')[0]
    old_lowscore = scores.get('low')[0]
    old_lowestscore = scores.get('lowest')[0]

    if (int(score) >= int(scores.get('high')[0])):
        scores['high'][0] = score
        scores['mid'][0] = old_highscore
        scores['low'][0] = old_midscore
        scores['lowest'][0] = old_lowscore
    elif (int(score) >= int(scores.get('mid')[0])):
        scores['mid'][0] = score
        scores['low'][0] = old_midscore
        scores['lowest'][0] = old_lowscore
    elif (int(score) >= int(scores.get('low')[0])):
        scores['low'][0] = score
        scores['lowest'][0] = old_lowscore
        scores['lowestest'][0] = old_lowestscore
    elif (int(score) >= int(scores.get('lowest')[0])):
        scores['lowest'][0] = score
        scores['lowestest'][0] = old_lowestscore

    write_highscore(file_name, scores)
