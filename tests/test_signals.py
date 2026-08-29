from mdas.analysis.signals import urgency_signal,churn_signal,toxicity_signal,sarcasm_signal

def test_signals():
    assert urgency_signal("Fix this immediately. It is urgent.")["score"]>0
    assert churn_signal("Fix this or I will cancel.")["score"]>0
    assert toxicity_signal("Your developers are idiots.")["score"]>0
    assert sarcasm_signal("Great job, another outage.")["method"]=="lexical_baseline"
