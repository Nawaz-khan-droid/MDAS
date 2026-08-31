import json
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path("src").resolve()))

from mdas.analyzer import MDASAnalyzer

prompts = [
    # --- SPAM / MALICIOUS (20) ---
    "CONGRATULATIONS! You have been selected to win a free iPhone 14! Click here http://scam.link to claim your prize now!!",
    "Viagra online fast shipping cheap prices. Buy now without prescription at medcheap.com",
    "URGENT: Your account has been compromised. Please login immediately to verify your identity: http://fake-login.com",
    "Make $5000 a week working from home! No experience needed. Email me to find out how.",
    "You have (1) new pending package delivery. Pay $2.99 shipping fee to release the package.",
    "Enlarge your business with our guaranteed SEO marketing services. We rank you #1 on Google.",
    "Claim your $1000 Walmart Gift Card by filling out this short 2 minute survey.",
    "Meet hot singles in your area tonight! 100% free registration.",
    "Your car warranty is about to expire. Press 1 to speak with an agent.",
    "Bitcoin investment returns guaranteed 500% in one week. Send BTC to this wallet.",
    "Dear user, your mailbox is almost full. Upgrade quota here: http://upgrade-mail.com",
    "Earn passive income while you sleep. Crypto trading bot guarantees profit.",
    "Hello dear, I am a widow from a royal family and I need your help to transfer $10 million...",
    "Flash sale! 90% off all Ray-Ban sunglasses for the next 2 hours only. Click here.",
    "Lose 20 pounds in one week with this miracle pill! Doctors hate it!",
    "Your PayPal account is limited. Please update your billing information.",
    "Notice of Tax Evasion: The IRS has filed a lawsuit against you. Call us immediately.",
    "Congratulations, your loan of $50,000 has been approved. Click to sign documents.",
    "You won the UK lottery! Reply with your bank details to process the transfer.",
    "Free followers and likes for your Instagram account. Enter your password here.",

    # --- BILLING / REFUNDS (20) ---
    "I was charged twice this month for my subscription. Please refund the extra $15 immediately.",
    "Where is my refund? It's been 5 days since you said it was processed.",
    "I'd like to cancel my subscription and get my money back. I haven't used the service.",
    "The invoice you sent for Order #9912 is incorrect. The total should be $45, not $60.",
    "Why did my monthly bill increase by $5? I was not notified of any price changes.",
    "I need to update my credit card on file before the next billing cycle.",
    "Can you send me a receipt for my last three transactions? I need them for taxes.",
    "I accidentally bought the wrong item. Can I cancel the order and get a refund?",
    "Your system says my payment failed, but my bank shows the money was deducted.",
    "I applied a discount code but it wasn't reflected in the final checkout price.",
    "How do I switch from a monthly billing plan to an annual billing plan?",
    "I dispute the charge of $99 on my account. This is fraudulent, I did not authorize it.",
    "When does my free trial end? Will I be automatically charged?",
    "I need to talk to someone about a discrepancy in my billing statement.",
    "Please close my account and refund the prorated amount for the remaining days.",
    "I paid for expedited shipping but it took a week. I want my shipping fee refunded.",
    "My corporate card was charged, but this should have gone to my personal card. Can we fix this?",
    "Are there any hidden fees if I downgrade my plan to the basic tier?",
    "The promotion clearly said 50% off, but I was charged full price.",
    "I'm trying to process a return for a defective item and get a full refund.",

    # --- TECHNICAL SUPPORT (20) ---
    "The application keeps crashing every time I try to export my report to PDF.",
    "I forgot my password and the password reset email is not arriving.",
    "My dashboard is loading extremely slowly since the latest update.",
    "Error code 500 keeps popping up when I try to save my profile settings.",
    "How do I integrate the API with my existing Python backend?",
    "The video playback stutters and buffers endlessly on my smart TV.",
    "I can't connect to the server. It says 'Connection timed out'.",
    "Where is the setting to enable two-factor authentication?",
    "The sync feature is completely broken. My mobile app doesn't match the web app.",
    "I'm getting a blank white screen when I log in on Google Chrome.",
    "Does this software support Mac OS? I can only find the Windows installer.",
    "The biometric login on my phone stopped working after I updated iOS.",
    "I need help configuring the webhook endpoints for my production environment.",
    "My data is corrupted. Is there a way to restore from yesterday's backup?",
    "The search function returns zero results even when I search for exact matches.",
    "I keep getting logged out randomly every 5 minutes. It's very frustrating.",
    "How do I clear the cache? The support doc says to go to settings but it's not there.",
    "The UI is completely misaligned on my iPad, buttons are overlapping.",
    "Whenever I upload an image larger than 2MB, the app freezes completely.",
    "I need an engineer to look at my logs, the database connection keeps dropping.",

    # --- FEEDBACK / PRAISE (20) ---
    "I just wanted to say that your new update is fantastic. It saved me hours of work!",
    "The customer service rep, Sarah, was incredibly helpful and polite. Great job!",
    "I love using your product, it's the best tool in the market by far.",
    "Honestly, this is the most intuitive interface I have ever used. Kudos to the design team.",
    "Thank you so much for resolving my issue so quickly. You guys rock!",
    "Five stars! Will definitely recommend this software to all my colleagues.",
    "I'm very impressed with the speed and reliability of your hosting service.",
    "Just dropping by to say I appreciate the excellent documentation you provide.",
    "The new dark mode feature is absolutely gorgeous. My eyes thank you.",
    "Your product has completely transformed how our team collaborates. Amazing work.",
    "I was skeptical at first, but this is genuinely a life-changing app.",
    "Big shoutout to the dev team for shipping that feature request so fast!",
    "I've tried all your competitors and none of them even come close to your quality.",
    "This is a masterpiece of software engineering. Clean, fast, and bug-free.",
    "Thank you for keeping the pricing affordable for small startups like us.",
    "I never write reviews, but your customer support blew me away today. Exceptional.",
    "The onboarding process was seamless. I was set up and running in 5 minutes.",
    "I absolutely adore the new analytics dashboard. So much clearer now.",
    "You guys are setting the gold standard for SaaS companies.",
    "Simply brilliant. I couldn't be happier with my purchase.",

    # --- ACCOUNT / GENERAL INQUIRIES (20) ---
    "How do I change the primary email address on my account?",
    "Do you offer any discounts for students or non-profit organizations?",
    "Where can I find your terms of service and privacy policy?",
    "Can I transfer ownership of my workspace to another team member?",
    "What are your business hours for phone support?",
    "Is it possible to pause my account for 3 months while I travel?",
    "How do I permanently delete my account and all associated data?",
    "Can you tell me where your servers are physically located?",
    "I'd like to schedule a demo for my enterprise team next week.",
    "Do you have a roadmap for upcoming features this year?",
    "How many users are allowed on the Pro plan?",
    "Is your platform GDPR compliant? I need to know for legal reasons.",
    "Can I use my account on multiple devices simultaneously?",
    "I need to merge two separate accounts into one. Is that possible?",
    "What is the process for becoming a certified partner or reseller?",
    "How long do you retain data after an account is deactivated?",
    "Can I customize the branding or use a white-label version?",
    "I received an email about updating terms, what exactly changed?",
    "Are there any limitations on the API rate limits for the free tier?",
    "I'd like to request a new feature: ability to export to Excel."
]

def run_test():
    print("Initializing Analyzer...")
    analyzer = MDASAnalyzer.from_directory("models")
    
    results = []
    print("Running inference on 100 prompts...\n")
    
    for i, prompt in enumerate(prompts, 1):
        try:
            res = analyzer.analyze(prompt)
            data = res.to_dict()
            
            # Extract key classifications
            spam_label = "Spam" if data["radar"]["urgency"] > 9000 else data["classification"]["spam"]["label"] # Simplified check, actual model uses spam label
            spam_label = data["classification"]["spam"]["label"]
            sentiment = data["classification"]["sentiment"]["label"]
            intent = data["classification"]["intent"]["label"]
            category = data["classification"]["category"]["label"]
            
            results.append({
                "ID": i,
                "Prompt": prompt,
                "Spam": spam_label,
                "Sentiment": sentiment,
                "Intent": intent,
                "Category": category
            })
            sys.stdout.write(f"\rProcessed {i}/100")
            sys.stdout.flush()
        except Exception as e:
            print(f"\nError on prompt {i}: {e}")
            
    print("\n\nGenerating Markdown Report...")
    
    md_content = "# MDAS 100-Prompt Evaluation Report\n\n"
    md_content += "| ID | Prompt snippet | Spam? | Sentiment | Intent | Category |\n"
    md_content += "|---|---|---|---|---|---|\n"
    
    for r in results:
        snippet = r["Prompt"][:45] + ("..." if len(r["Prompt"]) > 45 else "")
        snippet = snippet.replace("|", "").replace("\n", " ")
        md_content += f"| {r['ID']} | {snippet} | {r['Spam']} | {r['Sentiment']} | {r['Intent']} | {r['Category']} |\n"
        
    with open("evaluation_report_v2.md", "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print("Done! Report saved to evaluation_report_v2.md")

if __name__ == "__main__":
    run_test()
