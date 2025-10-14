def duplicate_encode(word):
    #your code here
    words = {}
    for n in word.lower():
        words[n] = 0
    for i in range(len(word)):
        w = word[i].lower()
        for j in word:
            if w == j :
                words[w] +=1
    for k in word:
        if words[k] > 1:
            word = word.lower().replace(k , ")")
        word =word.lower().replace(k , "(")
    return word