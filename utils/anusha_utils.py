
def parse_articles(path):
    data = {}
    for i, filename in enumerate(os.listdir(path)):
        if(i%3==2):
            article_id = filename.split(".")[0][7:]
            data[article_id] = []
            with open(TRAIN_SET_PATH_TASK2+"/"+filename, 'r', encoding="utf8") as f:
                count = 1
                for j, line in enumerate(f):
                    if(j%2==0):
                        data[article_id].append([count, line[:-1]])
                        count = count+1
    return data
    
    
def get_labels_array(labels_dict):
    labels_array = np.array([])
    for article_id in labels_dict.keys():
        for sentence_id, label in labels_dict[article_id]:
            labels_array = np.append(labels_array, label)
    return labels_array
    
    
def process_text(model, text, attr_name="text"):
    nlp = model
    tokens = []
    for token in nlp(text):
        if token.orth_.isspace():
            continue
        elif token.like_url:
            tokens.append('URL')
        else:
            tokens.append(getattr(token, attr_name))
            
    return tokens