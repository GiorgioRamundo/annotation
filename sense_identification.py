from sklearn.metrics import cohen_kappa_score


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

def nasari2():
    vector = nasari()
    result = {}
    for key in vector:
        result[vector[key][0]] = (key,vector[key][1])
    return result


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
            list.append((v[key][0],res)) # append float array in list result
    return list


def cos_sim(v1,v2):
    return product(v1,v2)/euclide(v1,v2)


# calculate similarity between babel synsets s1 e s2 using nasari
def similarity(babel_synset1,babel_synset2):
    v = nasari2()
    s = search(babel_synset1,v)
    if not s:
        return 0
    strings_1 = s[0][1]
    list_1 = []
    for s in strings_1:
        list_1.append(float(s))
    s = search(babel_synset2, v)
    if not s:
        return 0
    strings_2 = s[0][1]
    list_2 = []
    for s in strings_2:
        list_2.append(float(s))
    return cos_sim(list_1,list_2)


def annotated_data():
    file = open("synset_annotated.tsv", "r")
    dict = {}
    for line in file:
        data = line.split("\t")
        value = (data[2],data[3],round(similarity(data[2],data[3])))
        dict[(data[0],data[1])] = value
    return dict

result = {}
ns = nasari()
annotated = annotated_data()
for key in annotated:
    v1 = search(key[0].lower(),ns)
    v2 = search(key[1].lower(),ns)
    max = 0
    for n,x in v1: # for each babel synset in nasari for first term
        for m,y in v2: # for each babel synset in nasari for second term
            cs = cos_sim(x,y) # calculate cosin similarity
            if cs > max:
                v1_sense = n
                v2_sense = m
                max = cs # retain the maximum value
    result[(key[0],key[1])] = (v1_sense,v2_sense,round(max))

print('Babel synsets from NASARI    : ' + str(result))
print('Babel synsets from annotation: ' + str(annotated))
pairs_1 = []
pairs_2 = []
for x,y in result:
    pairs_1.append(result[(x,y)][2])
print(pairs_1)
for x,y in annotated:
    pairs_2.append(annotated[(x,y)][2])
print(pairs_2)
print(cohen_kappa_score(pairs_1,pairs_2))