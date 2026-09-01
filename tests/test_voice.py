from mdas.analysis.voice import analyze_voice
class Morph:
    def get(self,key): return []
class T:
    def __init__(self,text,pos,dep,head=None, tag_=None):
        self.text=text
        self.pos_=pos
        self.dep_=dep
        self.head=head or self
        self.morph=Morph()
        self.tag_=tag_ or pos
        self.children = []
        self.i = 0
        self.doc = None
        self.start = 0
        self.end = 1
        self.lemma_ = text.lower()
        self.is_punct = False
        self.is_space = False
        self.subtree = [self]
class S:
    text="John wrote the report."
    def __iter__(self):
        v=T("wrote","VERB","ROOT"); s=T("John","PROPN","nsubj",v); o=T("report","NOUN","obj",v); return iter([s,v,o])
    def __len__(self):
        return 3
class D:
    sents=[S()]
    def __iter__(self):
        return iter([])
def test_voice():
    r=analyze_voice(D()); assert r["summary"]["active"]==1; assert r["sentences"][0]["voice"]=="Active"
