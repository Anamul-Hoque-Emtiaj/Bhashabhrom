import numpy as np

letters = ['ক','খ','গ','ঘ','চ','ছ','জ','ঝ','এ','ন','ও','ই'] 
punctuation = ['।','!', "'", '(', ')', ',', '-', '.', '/', ';', '?'] 
cat = [{'ক','খ'},{'গ','ঘ'},{'জ','ঝ'},{'ত','থ','ট','ঠ'},{'প','ফ'},{'র','ড়','ঢ়'},{'দ','ড','ধ','ঢ'},{'ব','ভ'},{'স','শ','ষ','চ','ছ'},
       {'ই','ঈ','ি','ী'},{'ও','উ','ো','ু','ূ','ঊ'},{'অ','আ','এ','ে','া'}] 

def genWord(size):
    word = ""
    while size>0:
        word+= np.random.choice(letters, 1)[0]
        size = size - 1
    return word

def isPunc(ch):
    for c in punctuation:
        if c == ch:
            return True
    return False

def hasPunc(word):
    for c in word:
        if isPunc(c):
            return True
    
    return False

def genPunc():
    return np.random.choice(punctuation, 1)[0]

def puncError(word):
    noisy_word = ""
    i = 0
    while i < len(word):
        if isPunc(word[i]):
            rand = np.random.uniform(0,1,1)
            if rand<0.33: #space before punctuation
                noisy_word += (' '+word[i])
            elif rand<0.66: #more than one punc punctuation
                noisy_word += ((word[i]*np.random.randint(1,5)))
            elif rand<0.9: #wrong punctuation
                noisy_word += (genPunc())
            else: #miss punctuation
                pass
        else:
            noisy_word += (word[i])
        i = i+1

    return noisy_word
def getChar(st):
    s = np.random.randint(0,len(st),1)[0]
    c = 0
    for ch in st:
        if c == s:
            return ch
        c = c + 1
def spellingError(sentence):
    wordList = sentence.split()
    noisy_sentence = ""
    s = np.random.randint(0,len(wordList),1)[0]
    c = 0
    cnt = 0
    for word in wordList:
        if c == s:

            if noisy_sentence != "":
                noisy_sentence += " "
            for ch in word:
                if cnt<2:
                    flg = False
                    for ct in cat:
                        for ch2 in ct:
                            if ch == ch2:
                                flg = True
                                cnt = cnt + 1
                                noisy_sentence += (getChar(ct-{ch}))
                                break
                        if flg:
                            break
                    if not flg:
                        noisy_sentence += ch
                else:
                    noisy_sentence += ch
        else:
            if noisy_sentence == "":
                noisy_sentence += (word)
            else:
                noisy_sentence += (" "+word)
        c = c+1
    return noisy_sentence

def noise(sentence, threshold):
    random = np.random.uniform(0,1,1)
    if abs(random - threshold) == 0.05:
        return sentence
    
    if sentence.count('$')>=2:
        return sentence
    
    wordList = sentence.split()
    random = np.random.uniform(0,1,1)
    noisy_sentence = ""
    if random<0.20: #spelling error 20%
        return spellingError(sentence)
    elif random<0.30:  #merge word error 10%
        if len(wordList)>=2:

            s = np.random.randint(1,len(wordList),1)[0]
            c = 0
            prevWord = None
            for word in wordList:
                if c == s-1:
                    prevWord = word
                elif c == s:
                    if noisy_sentence == "":
                        noisy_sentence += (prevWord+word)
                    else:
                        noisy_sentence += (" "+prevWord+word)
                else:
                    if noisy_sentence == "":
                        noisy_sentence += (word)
                    else:
                        noisy_sentence += (" "+word)
                c = c + 1
            return noisy_sentence
        else:
            return sentence
            
    elif random<0.40: #split word error 10%
        s = np.random.randint(0,len(wordList),1)[0]
        c = 0
        for word in wordList:
            if c == s:
                if len(word)==1:
                    newWord = word
                else:
                    ind = np.random.randint(1,len(word)-1,1)[0]
                    newWord = word[0:ind]+" "+word[ind:]

                if noisy_sentence == "":
                    noisy_sentence += (newWord)
                else:
                    noisy_sentence += (" "+newWord)
            else:
                if noisy_sentence == "":
                    noisy_sentence += (word)
                else:
                    noisy_sentence += (" "+word)
            c = c + 1
        return noisy_sentence
    elif random<0.50: #extra word error 10%
        s = np.random.randint(0,len(wordList),1)[0]
        c = 0
        for word in wordList:
            if c == s:
                if noisy_sentence == "":
                    noisy_sentence += (genWord(np.random.randint(1,6))+" "+word)
                else:
                    noisy_sentence += (" "+genWord(np.random.randint(1,6))+" "+word)
            else:
                if noisy_sentence == "":
                    noisy_sentence += (word)
                else:
                    noisy_sentence += (" "+word)
            c = c + 1
        
        return noisy_sentence
    elif random<0.60: #missed word error 10%
        if len(wordList)>1:
            s = np.random.randint(0,len(wordList),1)[0]
            c = 0
            for word in wordList:
                if c == s:
                    if s == len(wordList)-1:
                        noisy_sentence += " "
                else:
                    if noisy_sentence == "":
                        noisy_sentence += (word)
                    else:
                        noisy_sentence += (" "+word)
                c = c + 1
            
            return noisy_sentence
        
        else:
            return sentence
    elif random<0.70: #extra space error 10%
        if len(wordList)>1:
            s = np.random.randint(0,len(wordList),1)[0]
            c = 0
            for word in wordList:
                if c == s:
                    if noisy_sentence == "":
                        noisy_sentence += (word+" "*np.random.randint(1,3))
                    else:
                        noisy_sentence += (" "*np.random.randint(1,4)+word)
                else:
                    if noisy_sentence == "":
                        noisy_sentence += (word)
                    else:
                        noisy_sentence += (" "+word)
                c = c + 1
            
            return noisy_sentence
        
        else:
            return sentence+" "
    elif random<0.85 and len(wordList)>=2: #Hybrid error 15%
        sen1 = ""
        sen2 = ""
        spl = len(wordList)/2
        c = 0
        for word in wordList:
            if c<=spl:
                if sen1 == "":
                    sen1 += word
                else:
                    sen1 += (" "+word)
            else:
                if sen2 == "":
                    sen2 += word
                else:
                    sen2 += (" "+word)
            c = c + 1
        return noise(sen1,threshold)+" "+noise(sen2,threshold)
    else: #punctuation error 15%
        c = 0
        for word in wordList:
            if c>0:
                if noisy_sentence == "":
                    noisy_sentence += (word)
                else:
                    noisy_sentence += (" "+word)
            elif hasPunc(word):
                if noisy_sentence == "":
                    noisy_sentence += (puncError(word))
                else:
                    noisy_sentence += (" "+puncError(word))
                c = c + 1
            else:
                if noisy_sentence == "":
                    noisy_sentence += (word)
                else:
                    noisy_sentence += (" "+word)
        
        return noisy_sentence
    
def addNoise(sentence):
    try: 
        return noise(sentence,np.random.uniform(0,1,1)[0])
    except:
        return sentence

print(addNoise("আমি ভাত খাই।"))
print(addNoise("আমি ভাত খাই।"))
print(addNoise("অনেক বাতাস হচ্ছে।"))
print(addNoise("অনেক বাতাস হচ্ছে।"))
print(addNoise("আপনি কি আমাকে দেখেছেন?"))
print(addNoise("আপনি কি আমাকে দেখেছেন?"))
print(addNoise("ভাল লাগছে ক্লাস করতে।"))
print(addNoise("ভাল লাগছে ক্লাস করতে।"))
print(addNoise("বাংলাদেশ আমার জন্মভূমি।"))
print(addNoise("বাংলাদেশ আমার জন্মভূমি।"))
print(addNoise("অন্য কোনো মহিলা এক দূরত্বের মধ্যে পরপর আটটি বিশ্ব রেকর্ড স্থাপন করতে পারেননি।"))
print(addNoise("অন্য কোনো মহিলা এক দূরত্বের মধ্যে পরপর আটটি বিশ্ব রেকর্ড স্থাপন করতে পারেননি।"))

 

                    