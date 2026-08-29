URGENCY = {"urgent","urgently","immediately","asap","now","critical","emergency","deadline","today","right away","cannot wait","can't wait"}
CHURN = {"cancel","cancellation","unsubscribe","leave","switch","competitor","competitors","terminate","close my account","delete my account","moving to another","take my business elsewhere"}
TOXIC = {"idiot","idiots","stupid","garbage","trash","moron","loser","shut up","screw you","damn","hell"}
SARCASM = {"great job","fantastic","wonderful","stellar","brilliant","what a surprise","love that","excellent work"}
NEGATIVE = {"bad","terrible","awful","horrible","unacceptable","angry","frustrated","hate","failed","failure","broken","worst","disappointed","ridiculous","useless","garbage"}

def _count(text, phrases):
    low = text.lower(); return sum(low.count(x) for x in phrases)

def _bounded(x): return round(max(0.0, min(1.0, x)), 3)

def urgency_signal(text):
    n = _count(text, URGENCY); s = _bounded(n/3)
    return {"score":s,"label":"high" if s>=.67 else "medium" if s>=.34 else "low","method":"lexical_baseline","evidence_count":n}

def churn_signal(text):
    n = _count(text, CHURN); s = _bounded(n/2)
    return {"score":s,"label":"high" if s>=.67 else "medium" if s>=.34 else "low","method":"lexical_baseline","evidence_count":n}

def toxicity_signal(text):
    n = _count(text, TOXIC); s = _bounded(n/3)
    return {"score":s,"label":"high" if s>=.67 else "medium" if s>=.34 else "low","method":"lexical_baseline","evidence_count":n}

def sarcasm_signal(text):
    n = _count(text, SARCASM); low=text.lower()
    bonus = .25 if n and any(w in low for w in NEGATIVE) else 0.0
    s = _bounded(min(.75,n*.25)+bonus)
    return {"score":s,"label":"likely" if s>=.67 else "possible" if s>=.34 else "low","method":"lexical_baseline","marker_count":n,"warning":"Sarcasm is context-dependent; this V1 score is not a calibrated probability."}

def sentiment_signal_from_label(label):
    if label is None: return None
    x=label.lower()
    return {"negative":1.0,"neutral":0.5,"positive":0.0}.get(x)

def build_signals(text, sentiment_label):
    return {"urgency":urgency_signal(text),"churn_risk":churn_signal(text),"toxicity":toxicity_signal(text),"sarcasm":sarcasm_signal(text),"sentiment_source":{"method":"classification_model","label":sentiment_label}}
