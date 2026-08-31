"""Accurate clause-level English active/passive/linking voice analysis."""

def get_clause_bounds(head, sent):
    # Get all tokens in the subtree of the head that belong to this sentence
    tokens = [t for t in head.subtree if t.i >= sent.start and t.i < sent.end]
    if not tokens:
        return sent.start, sent.end - 1
        
    min_i = min([t.i for t in tokens])
    max_i = max([t.i for t in tokens])
    
    # Trim leading coordinating conjunctions and punctuation
    while min_i <= max_i and (sent.doc[min_i].is_punct or sent.doc[min_i].dep_ == "cc" or sent.doc[min_i].is_space):
        min_i += 1
    # Trim trailing punctuation
    while max_i >= min_i and (sent.doc[max_i].is_punct or sent.doc[max_i].is_space):
        max_i -= 1
        
    if min_i > max_i:
        return sent.start, sent.end - 1
    return min_i, max_i

def extract_evidence(head, subj, is_imperative=False):
    details = {
        "text": "",
        "subject": subj.text if subj and not is_imperative else None,
        "verb": None,
        "aux": None,
        "object": None,
        "agent": None,
        "copula": None,
        "complement": None
    }
    
    tokens = []
    if subj and not is_imperative:
        tokens.append(subj)
    if head:
        tokens.append(head)
        if head.pos_ in {"VERB", "AUX"}:
            details["verb"] = head.text
        elif head.pos_ in {"ADJ", "NOUN", "PROPN"}:
            details["complement"] = head.text
    
    for c in head.children:
        if c.dep_ in {"aux", "auxpass", "neg", "prt"}:
            tokens.append(c)
            if c.dep_ in {"aux", "auxpass"} and details["aux"] is None:
                details["aux"] = c.text
        elif c.dep_ == "cop":
            tokens.append(c)
            details["copula"] = c.text
        elif c.dep_ in {"dobj"}:
            tokens.append(c)
            details["object"] = c.text
        elif c.dep_ in {"acomp", "attr"}:
            tokens.append(c)
            details["complement"] = c.text
        elif c.dep_ in {"agent", "obl:agent"}:
            tokens.append(c)
            for gc in c.children:
                if gc.dep_ == "pobj":
                    tokens.append(gc)
                    details["agent"] = gc.text
                    break
                    
    if subj and subj == head:
        for c in subj.children:
             if c.dep_ in {"cop", "aux"}:
                 tokens.append(c)
                 if c.dep_ == "cop": details["copula"] = c.text
                 if c.dep_ in {"aux"}: details["aux"] = c.text

    tokens = sorted(list(set(tokens)), key=lambda x: x.i)
    details["text"] = " ".join([t.text for t in tokens])
    return details

def _analyze_clauses(sent, start_id):
    clauses = []
    
    # Find all distinct subjects in the sentence
    subjects = [t for t in sent if t.dep_ in {"nsubj", "nsubjpass", "csubj", "csubjpass", "expl"}]
    
    for subj in subjects:
        head = subj.head
        is_passive = False
        is_linking = False
        
        # Passive Check
        if subj.dep_ in {"nsubjpass", "csubjpass"}:
            is_passive = True
        elif any(c.dep_ in {"auxpass", "aux:pass"} for c in head.children):
            is_passive = True
        elif head.tag_ == "VBN" and any(c.lemma_ in {"be", "get"} for c in head.children):
            is_passive = True
            
        # Linking Check
        if not is_passive:
            if head.pos_ in {"ADJ", "NOUN", "PROPN"} and any(c.dep_ == "cop" for c in head.children):
                is_linking = True
            elif head.lemma_ in {"be", "seem", "look", "appear", "feel", "become", "remain"} and any(c.dep_ in {"acomp", "attr"} for c in head.children):
                is_linking = True
        else:
            # Reclassify stative passives as Linking if they describe a state without an agent
            stative_participles = {"damage", "break", "tear", "close", "lose"}
            has_agent = any(c.dep_ in {"agent", "obl:agent"} for c in head.children)
            if not has_agent and head.lemma_ in stative_participles and any(c.lemma_ == "be" and c.tag_ in {"VBZ", "VBP"} for c in head.children):
                is_passive = False
                is_linking = True
                
        label = "Passive" if is_passive else ("Linking" if is_linking else "Active")
        
        evidence = extract_evidence(head, subj)
        min_i, max_i = get_clause_bounds(head, sent)
        text = sent.doc[min_i:max_i+1].text
        
        clauses.append({
            "segment_id": start_id + len(clauses),
            "text": text,
            "voice": label,
            "evidence": evidence
        })
        
    # If no clauses were found, fallback to checking for imperative (no subject)
    if not clauses:
        verbs = [t for t in sent if t.pos_ in {"VERB"}]
        if verbs:
            # find root verb
            root = next((t for t in sent if t.dep_ == "ROOT" and t.pos_ == "VERB"), verbs[0])
            if root.tag_ in {"VB", "VBP"} or "Imp" in root.morph.get("Mood", []):
                evidence = extract_evidence(root, None, is_imperative=True)
                clauses.append({
                    "segment_id": start_id,
                    "text": sent.text.strip(),
                    "voice": "Active",
                    "evidence": evidence
                })
                
    # If still nothing, it's uncertain
    if not clauses:
        clauses.append({
            "segment_id": start_id,
            "text": sent.text.strip(),
            "voice": "Uncertain",
            "evidence": "N/A"
        })
        
    return clauses

def analyze_voice(doc):
    segments = []
    current_id = 1
    for sent in doc.sents:
        clauses = _analyze_clauses(sent, current_id)
        segments.extend(clauses)
        current_id += len(clauses)
        
    counts = {"active": 0, "passive": 0, "linking": 0, "uncertain": 0}
    for item in segments:
        counts[item["voice"].lower()] += 1
        
    return {
        "summary": counts,
        "segments": segments
    }
