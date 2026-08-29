from mdas.analysis.statistics import analyze_statistics
class T:
    def __init__(self,text,alpha=False,punct=False): self.text=text; self.is_space=False; self.is_punct=punct; self.is_alpha=alpha; self.like_num=False
class S: pass
class D:
    text="Hello world."; sents=[S()]
    def __iter__(self): return iter([T("Hello",True),T("world",True),T(".",False,True)])
def test_statistics():
    r=analyze_statistics(D()); assert r["words"]==2; assert r["sentences"]==1
