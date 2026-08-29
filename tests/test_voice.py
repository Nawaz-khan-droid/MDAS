from mdas.analysis.voice import analyze_voice
class Morph:
    def get(self,key): return []
class T:
    def __init__(self,text,pos,dep,head=None): self.text=text; self.pos_=pos; self.dep_=dep; self.head=head or self; self.morph=Morph()
class S:
    text="John wrote the report."
    def __iter__(self):
        v=T("wrote","VERB","ROOT"); s=T("John","PROPN","nsubj",v); o=T("report","NOUN","obj",v); return iter([s,v,o])
class D:
    sents=[S()]
def test_voice():
    r=analyze_voice(D()); assert r["summary"]["active"]==1; assert r["sentences"][0]["voice"]=="Active"
