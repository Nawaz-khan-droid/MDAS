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
class SliceView:
    def __init__(self, tokens):
        self._tokens = tokens
        self.text = " ".join(t.text for t in tokens)
class S:
    text="John wrote the report."
    start = 0
    end = 3
    def __init__(self):
        self.doc = self
    def __iter__(self):
        v=T("wrote","VERB","ROOT"); s=T("John","PROPN","nsubj",v); o=T("report","NOUN","obj",v); return iter([s,v,o])
    def __len__(self):
        return 3
    def __getitem__(self, i):
        tokens = list(self.__iter__())
        if isinstance(i, slice):
            return SliceView(tokens[i])
        return tokens[i]
class D:
    sents=[S()]
    def __iter__(self):
        return iter([])
def test_voice():
    r=analyze_voice(D()); assert r["summary"]["active"]==1; assert r["segments"][0]["voice"]=="Active"
