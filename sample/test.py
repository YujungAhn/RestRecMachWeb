from modeling.modeling import recommandRes
from publicData import publicData


def test():
    ctprvnCds = publicData.getCtprvnCds()
    SignguCds = publicData.getSignguCds('41')
    AdongCds = publicData.getAdongCds('41117')

    areaCd = '41117600'
    name = '감성타코'
    resCount = 5 #가져오고 싶은 유사한 레스토랑 개수
    resList = recommandRes(name, areaCd, resCount)
    print(resList)