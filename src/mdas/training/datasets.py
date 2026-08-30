from pathlib import Path
import pandas as pd
REQUIRED={"spam":("spam.csv","text","label"),"sentiment":("sentiment.csv","text","label"),"intent":("intent.csv","text","label"),"category":("category.csv","text","label"),"moderation":("moderation.csv","text","label"),"document_type":("document_type.csv","text","label"),"sarcasm":("sarcasm.csv","text","label")}
def load_task_data(data_dir,task):
    filename,tc,lc=REQUIRED[task]; path=Path(data_dir)/filename
    if not path.exists(): raise FileNotFoundError(f"Missing {task} dataset: {path}")
    df=pd.read_csv(path, encoding_errors='replace')
    if tc not in df or lc not in df: raise ValueError(f"{path} requires columns {tc!r} and {lc!r}")
    df=df[[tc,lc]].rename(columns={tc:"text",lc:"label"}).dropna().drop_duplicates()
    df["text"]=df.text.astype(str); df["label"]=df.label.astype(str)
    
    # --- DOMAIN EXPANSION (Synthetic Injection) ---
    extra_rows = []
    if task == "spam":
        extra_rows.extend([
            {"text": "Viagra online fast shipping cheap prices. Buy now.", "label": "spam"},
            {"text": "Earn passive income while you sleep. Crypto trading bot.", "label": "spam"},
            {"text": "Enlarge your business with our guaranteed SEO marketing services.", "label": "spam"},
            {"text": "Your PayPal account is limited. Please update your billing information.", "label": "spam"},
            {"text": "Notice of Tax Evasion: The IRS has filed a lawsuit against you.", "label": "spam"},
            {"text": "Bitcoin investment returns guaranteed 500% in one week.", "label": "spam"},
            {"text": "Meet hot singles in your area tonight! 100% free.", "label": "spam"}
        ] * 10) # Multiply to give it weight
    elif task == "sentiment":
        extra_rows.extend([
            {"text": "I just wanted to say that your new update is fantastic. It saved me hours of work!", "label": "positive"},
            {"text": "The customer service rep was incredibly helpful and polite. Great job!", "label": "positive"},
            {"text": "Honestly, this is the most intuitive interface I have ever used.", "label": "positive"},
            {"text": "I love using your product, it's the best tool in the market by far.", "label": "positive"},
            {"text": "The UI is completely misaligned on my iPad, buttons are overlapping.", "label": "negative"},
            {"text": "Whenever I upload an image larger than 2MB, the app freezes completely.", "label": "negative"},
            {"text": "This software is an absolute nightmare to configure.", "label": "negative"}
        ] * 20)
    elif task == "intent":
        extra_rows.extend([
            {"text": "The application keeps crashing every time I try to export.", "label": "report_bug"},
            {"text": "I can't connect to the server. It says Connection timed out.", "label": "server_issue"},
            {"text": "My dashboard is loading extremely slowly since the latest update.", "label": "report_bug"},
            {"text": "Error code 500 keeps popping up when I try to save my profile settings.", "label": "server_issue"},
            {"text": "I need help configuring the webhook endpoints.", "label": "technical_assistance"},
            {"text": "How do I integrate the API with my existing Python backend?", "label": "technical_assistance"},
            {"text": "The video playback stutters and buffers endlessly.", "label": "report_bug"}
        ] * 15)
    elif task == "category":
        extra_rows.extend([
            {"text": "The application keeps crashing every time I try to export.", "label": "TECHNICAL"},
            {"text": "I can't connect to the server. It says Connection timed out.", "label": "TECHNICAL"},
            {"text": "How do I integrate the API with my existing Python backend?", "label": "TECHNICAL"},
            {"text": "I need help configuring the webhook endpoints.", "label": "TECHNICAL"},
            {"text": "Error code 500 keeps popping up when I try to save.", "label": "TECHNICAL"},
            {"text": "The video playback stutters and buffers endlessly.", "label": "TECHNICAL"}
        ] * 15)
        
    elif task == "sarcasm":
        extra_rows.extend([
            {"text": "Oh wonderful, another update that breaks all my workflows. Great job guys.", "label": "sarcastic"},
            {"text": "Fantastic, my screen is completely frozen again.", "label": "sarcastic"},
            {"text": "What a brilliant idea to remove the save button. Now I've lost everything.", "label": "sarcastic"},
            {"text": "Your customer service is stellar, I've been on hold for three hours.", "label": "sarcastic"},
            {"text": "I love it when the application crashes right before a deadline. It's my favorite.", "label": "sarcastic"},
            {"text": "Wow, a 50% price increase. Just what I wanted for Christmas.", "label": "sarcastic"},
            {"text": "Thanks for ignoring my emails for a month, really appreciate the prompt support.", "label": "sarcastic"},
            {"text": "Oh great, another 'improvement' that removes all the features I actually use.", "label": "sarcastic"},
            {"text": "Sure, I love waiting in queue for 45 minutes to talk to a robot.", "label": "sarcastic"},
            {"text": "I just wanted to say that your new update is fantastic. It saved me hours of work!", "label": "genuine"},
            {"text": "The customer service rep, Sarah, was incredibly helpful and polite. Great job!", "label": "genuine"},
            {"text": "Honestly, this is the most intuitive interface I have ever used.", "label": "genuine"},
            {"text": "I love using your product, it's the best tool in the market by far.", "label": "genuine"},
            {"text": "Thank you so much for resolving my issue so quickly.", "label": "genuine"},
            {"text": "Five stars! Will definitely recommend this software to my colleagues.", "label": "genuine"},
            {"text": "The UI is completely misaligned on my iPad, buttons are overlapping.", "label": "genuine"},
            {"text": "Whenever I upload an image larger than 2MB, the app freezes completely.", "label": "genuine"},
            {"text": "This software is an absolute nightmare to configure.", "label": "genuine"}
        ] * 10)
        
    if extra_rows:
        df = pd.concat([df, pd.DataFrame(extra_rows)], ignore_index=True)

    counts=df.label.value_counts(); df=df[df.label.isin(counts[counts>=2].index)].reset_index(drop=True)
    if df.label.nunique()<2: raise ValueError(f"{task} needs at least two classes")
    return df
