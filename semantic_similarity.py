def nasari():
    file = open("mini_NASARI.tsv","r") # vettori NASARI sono N-dimensionali, con N=300
    c = 0
    nasari = {}
    for line in file:
        data = line.split("\t")
        name = data[0]
        data.remove(name)
        name_list = name.split('__')
        real_name = name_list[1].replace('_',' ')
        nasari[real_name.lower()] = (name_list[0],data)
        c = c + 1
    file.close()
    return nasari


def annotated_data():
    file = open("test_data_annotated_2.tsv", "r")
    dict = {}
    for line in file:
        data = line.split("\t")
        value = int(data[2])
        dict[(data[0],data[1])] = value
    return dict


def product(v1,v2):
    somma = 0
    for i in range(len(v1)):
        somma = somma + (v1[i]*v2[i])
    return somma


def euclide(v1,v2):
    somma = 0
    for i in range(len(v1)):
        somma = somma + ((v1[i] - v2[i])**2)
    return pow(somma,1/2)


def search(s,v):
    list = []
    for key in v:
        if s in key:
            array = v[key][1] # array of nasari values
            res = []
            for a in array: # convert array of nasari values in a float array
                res.append(float(a))
            list.append(res) # append float array in list result
    return list


def cos_sim(v1,v2):
    return product(v1,v2)/euclide(v1,v2)

def media(v):
    somma = 0
    for x in v:
        somma = somma + x
    return somma / len(v)


def dev_standard(v):
    m = media(v)
    temp = 0
    for i in range(len(v)):
        temp = temp + ((v[i]-m)**2)
    return pow(temp/len(v),1/2)


def covariance(x,y):
    media_x = media(x)
    media_y = media(y)
    temp = []
    for i in range(len(x)):
        temp.append((x[i]-media_x)*(y[i]-media_y))
    return media(temp)


def pearson(x,y):
    return covariance(x,y)/(dev_standard(x)*dev_standard(y))


result = {}
nasari = nasari()
annotated = annotated_data()
for key in annotated:
    v1 = search(key[0].lower(),nasari)
    v2 = search(key[1].lower(),nasari)
    max = 0
    for x in v1: # for each babel synset in nasari for first term
        for y in v2: # for each babel synset in nasari for second term
            cs = cos_sim(x,y) # calculate cosin similarity
            if cs > max:
                max = cs # retain the maximum value
    result[(key[0],key[1])] = round(max)

print('Result from NASARI: ' + str(result))
print('Result from annotation: ' + str(annotated))
list_result = []
list_annotated = []
for key in result:
    list_result.append(result.get(key))
for key in annotated:
    list_annotated.append(annotated.get(key))
print('Pearson coefficient: ' + str(pearson(list_result,list_annotated)))