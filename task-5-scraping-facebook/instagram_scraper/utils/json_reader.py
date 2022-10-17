import json

def charCorrector(word:str):
    char_dict = {'ã¼' : 'ü', 
                'åº' : 'ź', 
                'ã¢' : 'â', 
                'ãº' : 'ú', 
                'ã²' : 'ò', 
                'ä±' : 'ı', 
                'åÿ' : 'ş', 
                'ã³' : 'ó', 
                'ã¨' : 'è', 
                'ã¡' : 'á', 
                'ã©' : 'é', 
                'ãÿ' : 'ß', 
                'ã¿' : 'ÿ', 
                'ã±' : 'ñ', 
                'ã§' : 'ç', 
                'ã¬' : 'ì', 
                'ã«' : 'ë', 
                'ã£' : 'ã', 
                'ã¦' : 'æ', 
                'ã°' : 'ð', 
                'ã¶' : 'ö', 
                'ã¥ã' : 'å', 
                'ãµ' : 'õ', 
                'ã´' : 'ô', 
                'ã»' : 'û', 
                'ã½' : 'ý', 
                'ãª' : 'ê', 
                'ã®' : 'î', 
                'ã¾' : 'þ', 
                'ã¸' : 'ø', 
                'ã¤' : 'ä', 
                'ã¹' : 'ù', 
                'ã¯' : 'ï',
            }
    # print(f'word: {word}')
    res = word
    for k,v in char_dict.items():
        if word.find(k) != -1:
            # print(f'key {k}')
            # print(f'value {v}')
            res = word.replace(k,v)
            res = charCorrector(res) # recursive solution to find all the occurrences
            break
    # print(f"result {res}")
    return res

def read_json(file_path):
    f = open(file_path)
    data = json.load(f)
    f.close()

    encoded_data = {}
    for k in data.keys():
        encoded_data.update({k : []})
        for v in data[k]:
            encoded_data[k].append(charCorrector(v.lower()))
    return encoded_data