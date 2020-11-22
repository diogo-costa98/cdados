def rmLowSup(D,Cx, postfixDic,minSup):
    Lx = Cx
    for iset in Cx:
        if len(postfixDic[iset])/len(D) < minSup:
            Lx.remove(iset)
            postfixDic.pop(iset)
        
    return Lx, postfixDic


def createC1(D, minSup):
    C1 = []
    postfixDic={}
    lenD = len(D)

    for i in range(lenD):
        for idx, item in enumerate(D[i]):
            if tuple([item]) not in C1:
                postfixDic[tuple([item])]={}
                
                C1.append(tuple([item]))
            if i not in postfixDic[tuple([item])].keys():
                postfixDic[tuple([item])][i]=idx

    L1, postfixDic = rmLowSup(D, C1, postfixDic, minSup)              
    
    return L1, postfixDic


def genNewPostfixDic(D,Lk, prePost):
    postfixDic = {}

    for Ck in Lk:
        postfixDic[Ck]={}
        tgt = Ck[-1]
        prePostList = prePost[Ck[:-1]]
        for r_i in prePostList.keys():
            for c_i in range(prePostList[r_i]+1, len(D[r_i])):
                if D[r_i][c_i]==tgt:
                    postfixDic[Ck][r_i] = c_i
                    break
    return postfixDic


def psGen(D, Lk, postfixDic, minSup, minConf):
    retList = []
    lenD = len(D)
    for Ck in Lk:
        item_count = {}
        for i in postfixDic[Ck].keys():
            item_exsit={}
            for j in range(postfixDic[Ck][i]+1, len(D[i])):
                if D[i][j] not in item_count.keys():
                    item_count[D[i][j]]=0
                if D[i][j] not in item_exsit:
                    item_count[D[i][j]]+=1
                    item_exsit[D[i][j]]=True

        c_items = []

        for item in item_count.keys():
            if item_count[item]/lenD >= minSup and item_count[item]/len(postfixDic[Ck])>=minConf:
                c_items.append(item)
        
        for c_item in c_items:
            retList.append(Ck+tuple([c_item]))
    
    return retList


def PrefixSpan(D, minSup=0.5, minConf=0.5, sptNum=False):
    L1, postfixDic = createC1(D, minSup)

    Dic_L1 = [{x:len(postfixDic[x])} for x in L1]
    
    Dic_L = [Dic_L1]

    L = [L1]

    k=2
    while len(L[k-2])>0:
        Lk = psGen(D, L[k-2], postfixDic,minSup, minConf)
        postfixDic = genNewPostfixDic(D,Lk,postfixDic)
        Dic_Lk = [{x:len(postfixDic[x])} for x in Lk]

        L.append(Lk)
        Dic_L1.append(Dic_Lk)
        k+=1
    
    return Dic_L
