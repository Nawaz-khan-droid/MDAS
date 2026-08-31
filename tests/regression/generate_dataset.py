import json
import random

INTENTS = [
    'cancel_order', 'change_order', 'change_shipping_address',
    'check_cancellation_fee', 'check_invoice', 'check_payment_methods',
    'check_refund_policy', 'complaint', 'contact_customer_service',
    'contact_human_agent', 'create_account', 'delete_account',
    'delivery_options', 'delivery_period', 'edit_account', 'get_invoice',
    'get_refund', 'newsletter_subscription', 'payment_issue', 'place_order',
    'recover_password', 'registration_problems', 'review',
    'set_up_shipping_address', 'switch_account', 'track_order', 'track_refund'
]

# Generate 90 Ham prompts spanning various intents
prompts = [
    ("I need to cancel my order immediately.", "cancel_order", "ham"),
    ("Please abort my recent purchase.", "cancel_order", "ham"),
    ("Can I change the items in my order?", "change_order", "ham"),
    ("I want to update my order with a different color.", "change_order", "ham"),
    ("I need to ship this to my new apartment instead.", "change_shipping_address", "ham"),
    ("How do I update the delivery address on my account?", "change_shipping_address", "ham"),
    ("What is the fee if I cancel my subscription?", "check_cancellation_fee", "ham"),
    ("Do you charge a penalty for early cancellation?", "check_cancellation_fee", "ham"),
    ("Where can I see my past invoices?", "check_invoice", "ham"),
    ("I would like to review the invoice for my last purchase.", "check_invoice", "ham"),
    ("Do you accept PayPal?", "check_payment_methods", "ham"),
    ("What credit cards can I use on your site?", "check_payment_methods", "ham"),
    ("What is your return policy?", "check_refund_policy", "ham"),
    ("How many days do I have to request a refund?", "check_refund_policy", "ham"),
    ("The item arrived broken, this is unacceptable!", "complaint", "ham"),
    ("Your service is terrible, I am very disappointed.", "complaint", "ham"),
    ("I need help from customer service.", "contact_customer_service", "ham"),
    ("Can someone from support please assist me?", "contact_customer_service", "ham"),
    ("I want to speak to a real person.", "contact_human_agent", "ham"),
    ("Transfer me to a live agent.", "contact_human_agent", "ham"),
    ("How do I sign up for a new account?", "create_account", "ham"),
    ("I would like to register for your website.", "create_account", "ham"),
    ("Please close my account.", "delete_account", "ham"),
    ("I want to permanently delete my profile.", "delete_account", "ham"),
    ("What are the available shipping options?", "delivery_options", "ham"),
    ("Do you offer express delivery?", "delivery_options", "ham"),
    ("How long does shipping take?", "delivery_period", "ham"),
    ("When will my package arrive?", "delivery_period", "ham"),
    ("I need to change my profile name.", "edit_account", "ham"),
    ("How do I update my phone number in my profile?", "edit_account", "ham"),
    ("Please send me a copy of my invoice.", "get_invoice", "ham"),
    ("I need a receipt for tax purposes.", "get_invoice", "ham"),
    ("I would like my money back.", "get_refund", "ham"),
    ("Please process a refund for my last order.", "get_refund", "ham"),
    ("Sign me up for the weekly newsletter.", "newsletter_subscription", "ham"),
    ("I want to subscribe to your mailing list.", "newsletter_subscription", "ham"),
    ("My credit card was declined during checkout.", "payment_issue", "ham"),
    ("I am getting an error when trying to pay.", "payment_issue", "ham"),
    ("I want to buy the premium package.", "place_order", "ham"),
    ("How do I complete my purchase?", "place_order", "ham"),
    ("I forgot my password and can't log in.", "recover_password", "ham"),
    ("Please send a password reset link.", "recover_password", "ham"),
    ("The website keeps crashing when I try to sign up.", "registration_problems", "ham"),
    ("I can't create an account, it gives me a server error.", "registration_problems", "ham"),
    ("The shoes are amazing, highly recommended!", "review", "ham"),
    ("I love this product, it works perfectly.", "review", "ham"),
    ("I need to add a new delivery address.", "set_up_shipping_address", "ham"),
    ("How do I add a secondary address to my account?", "set_up_shipping_address", "ham"),
    ("I want to switch to my business account.", "switch_account", "ham"),
    ("How do I log into a different profile?", "switch_account", "ham"),
    ("Where is my package right now?", "track_order", "ham"),
    ("Can I get a tracking number for my shipment?", "track_order", "ham"),
    ("Has my refund been processed yet?", "track_refund", "ham"),
    ("When will the money be back in my bank?", "track_refund", "ham"),
    
    # Adding more to reach 90
    ("Abort my current purchase.", "cancel_order", "ham"),
    ("Change my order to a size large.", "change_order", "ham"),
    ("Send it to my work address instead.", "change_shipping_address", "ham"),
    ("Is there a fee for cancelling?", "check_cancellation_fee", "ham"),
    ("Show me my bill.", "check_invoice", "ham"),
    ("Can I pay with crypto?", "check_payment_methods", "ham"),
    ("Can I return this after 30 days?", "check_refund_policy", "ham"),
    ("This software is a piece of trash.", "complaint", "ham"),
    ("Help desk, please.", "contact_customer_service", "ham"),
    ("Get me a human now.", "contact_human_agent", "ham"),
    ("Open a new account for me.", "create_account", "ham"),
    ("Erase my data and account.", "delete_account", "ham"),
    ("Is next day shipping available?", "delivery_options", "ham"),
    ("How many days until it gets here?", "delivery_period", "ham"),
    ("Update my email address.", "edit_account", "ham"),
    ("Download my invoice.", "get_invoice", "ham"),
    ("Refund my credit card.", "get_refund", "ham"),
    ("Add me to the mailing list.", "newsletter_subscription", "ham"),
    ("Payment failed on step 3.", "payment_issue", "ham"),
    ("I want to order three of these.", "place_order", "ham"),
    ("Reset my password.", "recover_password", "ham"),
    ("The registration page is broken.", "registration_problems", "ham"),
    ("This is the best service I have ever used.", "review", "ham"),
    ("Set my default shipping address.", "set_up_shipping_address", "ham"),
    ("Change to my other profile.", "switch_account", "ham"),
    ("What is the status of my delivery?", "track_order", "ham"),
    ("Is my refund still pending?", "track_refund", "ham"),

    # Edge cases and tricky ones
    ("The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!", "complaint", "ham"),
    ("I moved to a new city, update my delivery details.", "change_shipping_address", "ham"),
    ("I can't remember my login details.", "recover_password", "ham"),
    ("Your application is crashing on launch.", "complaint", "ham"),
    ("I want to buy this right now.", "place_order", "ham"),
    ("Can I see the receipt for my last payment?", "get_invoice", "ham"),
    ("Cancel my account and refund my money.", "delete_account", "ham"),
    ("Send me the tracking link.", "track_order", "ham"),
    ("I am stuck on the sign-up page.", "registration_problems", "ham")
]

# Ensure we have exactly 90
prompts = prompts[:90]

# Add 10 Spam prompts
spam_prompts = [
    ("Buy cheap rolex watches today at http://spam.com", "unknown", "spam"),
    ("You have won a $1000 gift card! Click here to claim your prize.", "unknown", "spam"),
    ("Hot singles in your area are waiting for you.", "unknown", "spam"),
    ("Earn $5000 a week from home with this simple trick.", "unknown", "spam"),
    ("Your bank account has been locked. Verify your identity at this link.", "unknown", "spam"),
    ("Enlarge your size naturally within weeks!", "unknown", "spam"),
    ("Invest in this new crypto coin before it goes to the moon!", "unknown", "spam"),
    ("Get 90% off all designer handbags, limited time only.", "unknown", "spam"),
    ("Urgent: Your package could not be delivered. Pay the fee here.", "unknown", "spam"),
    ("Congratulations! You are our 1 millionth visitor.", "unknown", "spam")
]

final_dataset = []
for p, intent, spam in (prompts + spam_prompts):
    final_dataset.append({
        "text": p,
        "expected_intent": intent,
        "expected_spam": spam
    })

with open("tests/regression/classification_100.json", "w") as f:
    json.dump(final_dataset, f, indent=2)

print(f"Generated {len(final_dataset)} test cases in classification_100.json")
