import numpy as np
punctuation = ["।", ",", "?","!",".",";","ঃ","-"]
def isPunc(ch):
    for c in punctuation:
        if c == ch:
            return True
    return False



def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            a = distances[t1][t2 - 1]
            b = distances[t1 - 1][t2]
            c = distances[t1 - 1][t2 - 1]
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = min(a+1,b+1,c)
            else:
                distances[t1][t2] = min(a+1,b+1,c+1)

    i = len(token1)
    j = len(token2)
    str = ""
    while i!=0 and j!=0:
        t = min(distances[i-1][j-1],distances[i][j-1],distances[i-1][j])
        if t == distances[i-1][j-1]:
            if token1[i-1] == token2[j-1]:
                str += token1[i-1]
            else:
                if isPunc(token1[i-1]):
                    str += 'r'
                else:
                    str += 's'
            i = i-1
            j = j-1
        elif t == distances[i][j-1]:
            if isPunc(token2[j-1]):
                str += 'p'
            else:
                
                if token2[j-1] == ' ':
                    str += 'x'
                else:
                    str += 'i'
            j = j-1
        else:
            if isPunc(token1[i-1]):
                str += 'q'
            else:
                
                if token1[i-1] == ' ':
                    str += 'y'
                else:
                    str += 'd'
            i = i-1
    
    if i==0 :
        while j!=0:
            if isPunc(token2[j-1]):
                str += 'p'
            else:
                
                if token2[j-1] == ' ':
                    str += 'x'
                else:
                    str += 'i'
            j = j-1
    
    if j==0 :
        while i!=0:
            if isPunc(token1[i-1]):
                str += 'q'
            else:
                
                if token1[i-1] == ' ':
                    str += 'y'
                else:
                    str += 'd'
            i = i-1

    str = str[::-1]      
    strList2 = str.split()
    strList = []
    
    for li in strList2:
        fi = False
        ci = 0
        ii = 0
        for ch in li:
            if ch == 'i' or ch == 'p' or ch == 's' or ch == 'r':
                ci += 1
                fi = True
            elif ch == 'x' :
                if fi:
                    strList.append(li[ii:ii+ci])
                    ii += (ci +1)
                    fi = False
                    ci = 0
                else:
                    li = li[ii:]
                    break
            else:
                li = li[ii:]
                break
            

        fd = False
        cd = 0
        ii = 0
        for ch in li:
            if ch == 'd' or ch == 'q' or ch == 's' or ch == 'r':
                cd += 1
                fd = True
            elif ch == 'y':
                if fd:
                    strList.append(li[ii:ii+cd])
                    ii += (cd +1)
                    fd = False
                    cd = 0
                else:
                    li = li[ii:]
                    break
            else:
                li = li[ii:]
                break
        ii = 0
        pl = []
        for ch in li:
            if isPunc(ch) or ch == 'p' or ch == 'q' or ch == 'r':
                pl.append(ii)
            ii = ii + 1
        
        if len(pl) == 0:
            if len(li)>0:
                strList.append(li)
        else:
            ii = 0
            co = 0
            for pi in pl:
                co = co +1
                if co == len(pl):
                    if pi == len(li) -1:
                        strList.append(li[ii:])
                    else:
                        strList.append(li[ii:pi+1])
                        strList.append(li[pi+1:])
                elif isPunc(li[pi+1]) or li[pi+1] == 'p' or li[pi+1] == 'q' or li[pi+1] == 'r':
                   
                    continue
                else:
                    strList.append(li[ii:pi+1])
                    ii = pi+1
                

    i = 0
    fstr = ""
    #print(strList2)
    #print(strList)
    for st in strList:
        s1 = ""
        t = len(st)
        dc =0
        ic =0
        sc =0
        pic = 0
        pdc = 0
        psc = 0
        sic = 0
        sdc = 0
        pc = 0
        
        for ch in st:
            if ch == 'd':
                dc +=1
            if ch == 'i' :
                ic +=1
            if ch == 's':
                sc +=1
            if ch == 'p':
                pic +=1
            if ch == 'q':
                pdc +=1
            if ch == 'x':
                sic +=1
            if ch == 'y':
                sdc +=1
            if ch == 'r':
                psc +=1
            if isPunc(ch):
                pc+=1

        tc = ic+sc+dc+sic+sdc+pic+pdc+psc
        
        if tc>0:
            if len(st) == (ic+pic+sic):
                if fstr == "":
                    fstr += ("$$")
                else:
                    fstr += ("$$ ")
            elif len(st) == (dc+pdc+sdc):
                for it in range(t):
                    s1 += token1[i]
                    i = i+1

                    

                if i<len(token1) and token1[i] == ' ':
                    fstr += ("$"+s1+"$ ")
                    i = i+1
                else:
                    fstr += ("$"+s1+"$")
            else:
                for it in range(t-ic-pic-sic):
                    s1 += token1[i]
                    i = i+1

                s2 = s1.lstrip()
                if len(s1) - len(s2) == tc:
                    if i<len(token1) and token1[i] == ' ':
                        fstr += ("$"+(' '*(len(s1)-len(s2)))+"$"+s2+" ")
                        i = i+1
                    else:
                        fstr += ("$"+(' '*(len(s1)-len(s2)))+"$"+s2)
                    
                else:
                    if len(s1)>len(s2):
                        fstr += ("$"+(' '*(len(s1)-len(s2)))+"$")
                    tc2 = tc - (len(s1) - len(s2))
                    if (pc+pic+psc+pdc) == 0:
                        if i<len(token1) and token1[i] == ' ':
                            fstr += ("$"+s2+"$ ")
                            i = i+1
                        else:
                            fstr += ("$"+s2+"$")
                        
                    else:
                        if tc2 == 1 and st[len(st)-1] == 'p':
                            if i<len(token1) and token1[i] == ' ':
                                fstr += (s2+"$$ ")
                                i = i+1
                            else:
                                fstr += (s2+"$$")
                            
                        elif tc2 == 1 and isPunc(s2[len(s2)-1]) and (st[len(st)-1] == 'q' or st[len(st)-1] == 'r'):
                            if i<len(token1) and token1[i] == ' ':
                                fstr += (s2[0:-1]+"$"+s2[len(s2)-1]+"$ ")
                                i = i+1
                            else:
                                fstr += (s2[0:-1]+"$"+s2[len(s2)-1]+"$")
                            
                        else:
                            pi = len(s2)-1
                            ci = 0
                            lsi = -1
                            for cii in s2:
                                if cii == ' ' or cii == 'y':
                                    lsi = ci
                                if isPunc(cii) or cii =='p' or cii =='q' or cii =='r':
                                    pi = ci
                                    break
                                ci = ci + 1
                            if tc2 == (pic+psc+pdc):
                                
                                if i<len(token1) and token1[i] == ' ':
                                    fstr += (s2[0:pi]+"$"+s2[pi:]+"$ ")
                                    i = i+1
                                else:
                                    fstr += (s2[0:pi]+"$"+s2[pi:]+"$")
                                
                            else:
                                if lsi != pi-1:
                                    if (pic+psc+pdc) == 0:
                                        if i<len(token1) and token1[i] == ' ':
                                            fstr += ("$"+s2[0:pi]+"$"+s2[pi:]+" ")
                                            i = i+1
                                        else:
                                            fstr += ("$"+s2[0:pi]+"$"+s2[pi:])
                                        
                                    else:
                                        if i<len(token1) and token1[i] == ' ':
                                            fstr += ("$"+s2[0:pi]+"$$"+s2[pi:]+"$ ")
                                            i = i+1
                                        else:
                                            fstr += ("$"+s2[0:pi]+"$$"+s2[pi:]+"$")
                                        
                                else:
                                    while s2[lsi] == ' ':
                                        lsi = lsi -1
                                        if lsi == -1:
                                            break
                                    lsi = lsi + 1
                                    if (pic+pdc+psc) == 0:
                                        if tc2 == (pi-lsi):
                                            if i<len(token1) and token1[i] == ' ':
                                                fstr += (s2[0:lsi]+"$"+s2[lsi:pi]+"$"+s2[pi:]+" ")
                                                i = i+1
                                            else:
                                                fstr += (s2[0:lsi]+"$"+s2[lsi:pi]+"$"+s2[pi:])
                                            
                                        else:
                                            if i<len(token1) and token1[i] == ' ':
                                                fstr += ("$"+s2[0:lsi]+"$$"+s2[lsi:pi]+"$"+s2[pi:]+" ")
                                                i = i+1
                                            else:
                                                fstr += ("$"+s2[0:lsi]+"$$"+s2[lsi:pi]+"$"+s2[pi:])
                                    else:
                                        if tc2 == ((pi-lsi)+pic+pdc+psc):
                                            if i<len(token1) and token1[i] == ' ':
                                                fstr += (s2[0:lsi]+"$"+s2[lsi:pi]+"$$"+s2[pi:]+"$ ")
                                                i = i+1
                                            else:
                                                fstr += (s2[0:lsi]+"$"+s2[lsi:pi]+"$$"+s2[pi:]+"$")
                                            
                                        else:
                                            if i<len(token1) and token1[i] == ' ':
                                                fstr += ("$"+s2[0:lsi]+"$$"+s2[lsi:pi]+"$$"+s2[pi:]+"$ ")
                                                i = i+1
                                            else:
                                                fstr += ("$"+s2[0:lsi]+"$$"+s2[lsi:pi]+"$$"+s2[pi:]+"$")
                
                
                               
                                        
        else:
            
            for it in range(t):
                s1 += token1[i]
                i = i+1
                    
            if i<len(token1) and token1[i] == ' ':
                i = i+1
                fstr += (s1+" ")
            else:
                fstr += (s1)
            
                
            #print(fstr)
    return fstr

def compare(str1, str2):
    try:
        return levenshteinDistanceDP(str1, str2)
    except:
        return str1
              

print(compare("আমী ভাত খাই।","আমি ভাত খাই।"))
print(compare("অনেক বাতাষ হচ্ছে।","অনেক বাতাস হচ্ছে।"))
print(compare("আপনি কি আমাকে দেখেছেন।","আপনি কি আমাকে দেখেছেন?"))
print(compare("আপনি কি রিক অ্যান্ড মর্টি দেখেছেন","আপনি কি রিক অ্যান্ড মর্টি দেখেছেন?"))
print(compare("ভাললাগছে ক্লাসকরতে।","ভাল লাগছে ক্লাস করতে।"))
print(compare("তুমি ভাত খাও ।","তুমি ভাত খাও।"))
print(compare("এটা কখনোই আমার পরিকল্পনা ছিল না।","এটা কখনই আমার পরিকল্পনা ছিল না।"))
print(compare("বাংলা ধেষ আমার জন্মভূমি।","বাংলাদেশ আমার জন্মভূমি।"))
print(compare("সে আমি তুমি স্কুলে যাই।","সে, আমি ও তুমি স্কুলে যাই।"))
print(compare("আমি ও স্কুলে যাই।","আমি স্কুলে যাই।"))
print(compare("সে,আমি,তুমি স্কুলে যাই।।।","সে, আমি ও তুমি স্কুলে যাই।"))
print(compare("অন্য   কোন মহিলা এক দূরত্বের মধ্যে পরপর আটটি বিশ্ব রেকর্ড স্থাপন করতে পারেননি।","অন্য কোনো মহিলা এক দূরত্বের মধ্যে পরপর আটটি বিশ্ব রেকর্ড স্থাপন করতে পারেননি।"))
