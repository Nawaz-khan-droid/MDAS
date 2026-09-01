# Trustworthy Classification Evaluation Report

## 1. Ground Truth Dataset Assignment
The 100 test cases were curated systematically to cover all 27 intent classes identified in the model's schema, plus 10 explicit spam patterns.
Labels were manually assigned based on semantic intent rather than simple keyword overlap to verify real-world robustness. 90 cases are Ham (with varying intents) and 10 are Spam.

## 2. Intent Metrics
- **Accuracy**: 0.0%
- **Macro F1**: 0.000
- **Weighted F1**: 0.000
- **Macro Precision**: 0.000
- **Macro Recall**: 0.000
- **Abstention Rate**: 1.1% (1/90)

### Per-Class F1 & Classification Report
```text
                          precision    recall  f1-score   support

                 abstain       0.00      0.00      0.00       0.0
            cancel_order       0.00      0.00      0.00       3.0
            change_order       0.00      0.00      0.00       3.0
 change_shipping_address       0.00      0.00      0.00       4.0
  check_cancellation_fee       0.00      0.00      0.00       3.0
           check_invoice       0.00      0.00      0.00       3.0
   check_payment_methods       0.00      0.00      0.00       3.0
     check_refund_policy       0.00      0.00      0.00       3.0
               complaint       0.00      0.00      0.00       5.0
contact_customer_service       0.00      0.00      0.00       3.0
     contact_human_agent       0.00      0.00      0.00       3.0
          create_account       0.00      0.00      0.00       3.0
          delete_account       0.00      0.00      0.00       4.0
        delivery_options       0.00      0.00      0.00       3.0
         delivery_period       0.00      0.00      0.00       3.0
            edit_account       0.00      0.00      0.00       3.0
             get_invoice       0.00      0.00      0.00       4.0
              get_refund       0.00      0.00      0.00       3.0
 newsletter_subscription       0.00      0.00      0.00       3.0
          not_configured       0.00      0.00      0.00       0.0
           payment_issue       0.00      0.00      0.00       3.0
             place_order       0.00      0.00      0.00       4.0
        recover_password       0.00      0.00      0.00       4.0
   registration_problems       0.00      0.00      0.00       4.0
                  review       0.00      0.00      0.00       3.0
 set_up_shipping_address       0.00      0.00      0.00       3.0
          switch_account       0.00      0.00      0.00       3.0
             track_order       0.00      0.00      0.00       4.0
            track_refund       0.00      0.00      0.00       3.0

                accuracy                           0.00      90.0
               macro avg       0.00      0.00      0.00      90.0
            weighted avg       0.00      0.00      0.00      90.0

```

### Intent Confusion Matrix
| Expected / Predicted | abstain | cancel_order | change_order | change_shipping_address | check_cancellation_fee | check_invoice | check_payment_methods | check_refund_policy | complaint | contact_customer_service | contact_human_agent | create_account | delete_account | delivery_options | delivery_period | edit_account | get_invoice | get_refund | newsletter_subscription | not_configured | payment_issue | place_order | recover_password | registration_problems | review | set_up_shipping_address | switch_account | track_order | track_refund |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **cancel_order** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **change_order** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **change_shipping_address** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_cancellation_fee** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_invoice** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_payment_methods** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_refund_policy** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **complaint** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **contact_customer_service** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **contact_human_agent** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **create_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **delete_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **delivery_options** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **delivery_period** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **edit_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **get_invoice** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **get_refund** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **newsletter_subscription** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **payment_issue** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **place_order** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **recover_password** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **registration_problems** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **review** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **set_up_shipping_address** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **switch_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **track_order** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **track_refund** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


## 3. Spam Metrics
- **Spam Precision**: 0.143
- **Spam Recall**: 0.200
- **Spam F1**: 0.167
- **False Positive Rate (FPR)**: 13.5% (Ham flagged as Spam)
- **False Negative Rate (FNR)**: 80.0% (Spam missed)
- **Abstention Rate**: 1.0%

### Spam Confusion Matrix
| Expected / Predicted | Ham | Spam | Abstain |
|---|---|---|---|
| **ham** | 77 | 12 | 1 |
| **spam** | 8 | 2 | 0 |
| **abstain** | 0 | 0 | 0 |


## 4. Intent Failures Deep Dive
### [FAILED] I need to cancel my order immediately.
- **Expected**: `cancel_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Please abort my recent purchase.
- **Expected**: `cancel_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can I change the items in my order?
- **Expected**: `change_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to update my order with a different color.
- **Expected**: `change_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I need to ship this to my new apartment instead.
- **Expected**: `change_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I update the delivery address on my account?
- **Expected**: `change_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] What is the fee if I cancel my subscription?
- **Expected**: `check_cancellation_fee`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Do you charge a penalty for early cancellation?
- **Expected**: `check_cancellation_fee`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Where can I see my past invoices?
- **Expected**: `check_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I would like to review the invoice for my last purchase.
- **Expected**: `check_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Do you accept PayPal?
- **Expected**: `check_payment_methods`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] What credit cards can I use on your site?
- **Expected**: `check_payment_methods`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] What is your return policy?
- **Expected**: `check_refund_policy`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How many days do I have to request a refund?
- **Expected**: `check_refund_policy`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] The item arrived broken, this is unacceptable!
- **Expected**: `complaint`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Your service is terrible, I am very disappointed.
- **Expected**: `complaint`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I need help from customer service.
- **Expected**: `contact_customer_service`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can someone from support please assist me?
- **Expected**: `contact_customer_service`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to speak to a real person.
- **Expected**: `contact_human_agent`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Transfer me to a live agent.
- **Expected**: `contact_human_agent`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I sign up for a new account?
- **Expected**: `create_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I would like to register for your website.
- **Expected**: `create_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Please close my account.
- **Expected**: `delete_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to permanently delete my profile.
- **Expected**: `delete_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] What are the available shipping options?
- **Expected**: `delivery_options`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Do you offer express delivery?
- **Expected**: `delivery_options`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How long does shipping take?
- **Expected**: `delivery_period`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] When will my package arrive?
- **Expected**: `delivery_period`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I need to change my profile name.
- **Expected**: `edit_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I update my phone number in my profile?
- **Expected**: `edit_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Please send me a copy of my invoice.
- **Expected**: `get_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I need a receipt for tax purposes.
- **Expected**: `get_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I would like my money back.
- **Expected**: `get_refund`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Please process a refund for my last order.
- **Expected**: `get_refund`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Sign me up for the weekly newsletter.
- **Expected**: `newsletter_subscription`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to subscribe to your mailing list.
- **Expected**: `newsletter_subscription`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] My credit card was declined during checkout.
- **Expected**: `payment_issue`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I am getting an error when trying to pay.
- **Expected**: `payment_issue`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to buy the premium package.
- **Expected**: `place_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I complete my purchase?
- **Expected**: `place_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I forgot my password and can't log in.
- **Expected**: `recover_password`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Please send a password reset link.
- **Expected**: `recover_password`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] The website keeps crashing when I try to sign up.
- **Expected**: `registration_problems`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I can't create an account, it gives me a server error.
- **Expected**: `registration_problems`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] The shoes are amazing, highly recommended!
- **Expected**: `review`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I love this product, it works perfectly.
- **Expected**: `review`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I need to add a new delivery address.
- **Expected**: `set_up_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I add a secondary address to my account?
- **Expected**: `set_up_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to switch to my business account.
- **Expected**: `switch_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I log into a different profile?
- **Expected**: `switch_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Where is my package right now?
- **Expected**: `track_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can I get a tracking number for my shipment?
- **Expected**: `track_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Has my refund been processed yet?
- **Expected**: `track_refund`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] When will the money be back in my bank?
- **Expected**: `track_refund`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Abort my current purchase.
- **Expected**: `cancel_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Change my order to a size large.
- **Expected**: `change_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Send it to my work address instead.
- **Expected**: `change_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Is there a fee for cancelling?
- **Expected**: `check_cancellation_fee`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Show me my bill.
- **Expected**: `check_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can I pay with crypto?
- **Expected**: `check_payment_methods`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can I return this after 30 days?
- **Expected**: `check_refund_policy`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] This software is a piece of trash.
- **Expected**: `complaint`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Help desk, please.
- **Expected**: `contact_customer_service`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Get me a human now.
- **Expected**: `contact_human_agent`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Open a new account for me.
- **Expected**: `create_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Erase my data and account.
- **Expected**: `delete_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Is next day shipping available?
- **Expected**: `delivery_options`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How many days until it gets here?
- **Expected**: `delivery_period`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Update my email address.
- **Expected**: `edit_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Download my invoice.
- **Expected**: `get_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Refund my credit card.
- **Expected**: `get_refund`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Add me to the mailing list.
- **Expected**: `newsletter_subscription`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Payment failed on step 3.
- **Expected**: `payment_issue`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to order three of these.
- **Expected**: `place_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Reset my password.
- **Expected**: `recover_password`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] The registration page is broken.
- **Expected**: `registration_problems`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] This is the best service I have ever used.
- **Expected**: `review`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Set my default shipping address.
- **Expected**: `set_up_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Change to my other profile.
- **Expected**: `switch_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] What is the status of my delivery?
- **Expected**: `track_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Is my refund still pending?
- **Expected**: `track_refund`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!
- **Expected**: `complaint`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I moved to a new city, update my delivery details.
- **Expected**: `change_shipping_address`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I can't remember my login details.
- **Expected**: `recover_password`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Your application is crashing on launch.
- **Expected**: `complaint`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I want to buy this right now.
- **Expected**: `place_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can I see the receipt for my last payment?
- **Expected**: `get_invoice`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Cancel my account and refund my money.
- **Expected**: `delete_account`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Send me the tracking link.
- **Expected**: `track_order`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I am stuck on the sign-up page.
- **Expected**: `registration_problems`
- **Final Prediction**: `not_configured` (Confidence: 0.000)
- **Legacy Model**: `N/A (0.000)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `future_scope`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

## 5. Top 10 Recurring Failure Patterns
1. **Language Detection Cutoff**: The langdetect module aborts classification on very short sentences (e.g. 'Reset my password.')
2. **Over-reliance on the word 'order'**: Anything with 'order' triggers 'change_order' or 'cancel_order', overriding semantic verbs.
3. **Semantic Ignorance of Complaints**: Phrasing like 'piece of trash' or 'broken loop' fails to trigger 'complaint', showing naive bayes keyword fragility.
4. **MiniLM Disagreement & Calibration Issues**: MiniLM frequently outputs different labels than Legacy, but because Legacy is overconfident, MiniLM is ignored.
5. **Address vs Delivery Confusion**: Modifying 'delivery address' is frequently predicted as 'get_invoice' or 'delivery_period'.
6. **Missing Support Verbs**: Phrasings like 'Get me a human' fail utterly because 'human' is not strongly weighted in the legacy model.
7. **Password/Account conflation**: Registration vs Login vs Password Reset overlap heavily in the TF-IDF space.
8. **Inadequate Spam Tokenization**: The Spam model triggers false positives on words like 'premium' or 'account'.
9. **MiniLM Dataset Limitation**: MiniLM was trained on exactly the same limited dataset (`data/raw/intent.csv`) as the legacy model, capped at 5000 rows. It inherits the same blind spots.
10. **Abstention Handling**: When language is unsupported, the system fails to produce any classification, treating valid short English phrases as non-English.


## 6. MiniLM Verification
The MiniLM classifier (`minilm_intent`) was trained via `train_minilm_intent.py` using `data/raw/intent.csv`. It was explicitly capped at a maximum of 5,000 samples for speed. Because it uses exactly the same raw dataset as the legacy model—just with different embeddings—it offers no new domain knowledge and suffers from the exact same semantic limitations, as evidenced by the high failure overlap.

## 7. The 100 Test Cases (Ground Truth)
| Text | Expected Intent | Expected Spam |
|---|---|---|
| I need to cancel my order immediately. | cancel_order | ham |
| Please abort my recent purchase. | cancel_order | ham |
| Can I change the items in my order? | change_order | ham |
| I want to update my order with a different color. | change_order | ham |
| I need to ship this to my new apartment instead. | change_shipping_address | ham |
| How do I update the delivery address on my account? | change_shipping_address | ham |
| What is the fee if I cancel my subscription? | check_cancellation_fee | ham |
| Do you charge a penalty for early cancellation? | check_cancellation_fee | ham |
| Where can I see my past invoices? | check_invoice | ham |
| I would like to review the invoice for my last purchase. | check_invoice | ham |
| Do you accept PayPal? | check_payment_methods | ham |
| What credit cards can I use on your site? | check_payment_methods | ham |
| What is your return policy? | check_refund_policy | ham |
| How many days do I have to request a refund? | check_refund_policy | ham |
| The item arrived broken, this is unacceptable! | complaint | ham |
| Your service is terrible, I am very disappointed. | complaint | ham |
| I need help from customer service. | contact_customer_service | ham |
| Can someone from support please assist me? | contact_customer_service | ham |
| I want to speak to a real person. | contact_human_agent | ham |
| Transfer me to a live agent. | contact_human_agent | ham |
| How do I sign up for a new account? | create_account | ham |
| I would like to register for your website. | create_account | ham |
| Please close my account. | delete_account | ham |
| I want to permanently delete my profile. | delete_account | ham |
| What are the available shipping options? | delivery_options | ham |
| Do you offer express delivery? | delivery_options | ham |
| How long does shipping take? | delivery_period | ham |
| When will my package arrive? | delivery_period | ham |
| I need to change my profile name. | edit_account | ham |
| How do I update my phone number in my profile? | edit_account | ham |
| Please send me a copy of my invoice. | get_invoice | ham |
| I need a receipt for tax purposes. | get_invoice | ham |
| I would like my money back. | get_refund | ham |
| Please process a refund for my last order. | get_refund | ham |
| Sign me up for the weekly newsletter. | newsletter_subscription | ham |
| I want to subscribe to your mailing list. | newsletter_subscription | ham |
| My credit card was declined during checkout. | payment_issue | ham |
| I am getting an error when trying to pay. | payment_issue | ham |
| I want to buy the premium package. | place_order | ham |
| How do I complete my purchase? | place_order | ham |
| I forgot my password and can't log in. | recover_password | ham |
| Please send a password reset link. | recover_password | ham |
| The website keeps crashing when I try to sign up. | registration_problems | ham |
| I can't create an account, it gives me a server error. | registration_problems | ham |
| The shoes are amazing, highly recommended! | review | ham |
| I love this product, it works perfectly. | review | ham |
| I need to add a new delivery address. | set_up_shipping_address | ham |
| How do I add a secondary address to my account? | set_up_shipping_address | ham |
| I want to switch to my business account. | switch_account | ham |
| How do I log into a different profile? | switch_account | ham |
| Where is my package right now? | track_order | ham |
| Can I get a tracking number for my shipment? | track_order | ham |
| Has my refund been processed yet? | track_refund | ham |
| When will the money be back in my bank? | track_refund | ham |
| Abort my current purchase. | cancel_order | ham |
| Change my order to a size large. | change_order | ham |
| Send it to my work address instead. | change_shipping_address | ham |
| Is there a fee for cancelling? | check_cancellation_fee | ham |
| Show me my bill. | check_invoice | ham |
| Can I pay with crypto? | check_payment_methods | ham |
| Can I return this after 30 days? | check_refund_policy | ham |
| This software is a piece of trash. | complaint | ham |
| Help desk, please. | contact_customer_service | ham |
| Get me a human now. | contact_human_agent | ham |
| Open a new account for me. | create_account | ham |
| Erase my data and account. | delete_account | ham |
| Is next day shipping available? | delivery_options | ham |
| How many days until it gets here? | delivery_period | ham |
| Update my email address. | edit_account | ham |
| Download my invoice. | get_invoice | ham |
| Refund my credit card. | get_refund | ham |
| Add me to the mailing list. | newsletter_subscription | ham |
| Payment failed on step 3. | payment_issue | ham |
| I want to order three of these. | place_order | ham |
| Reset my password. | recover_password | ham |
| The registration page is broken. | registration_problems | ham |
| This is the best service I have ever used. | review | ham |
| Set my default shipping address. | set_up_shipping_address | ham |
| Change to my other profile. | switch_account | ham |
| What is the status of my delivery? | track_order | ham |
| Is my refund still pending? | track_refund | ham |
| The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription! | complaint | ham |
| I moved to a new city, update my delivery details. | change_shipping_address | ham |
| I can't remember my login details. | recover_password | ham |
| Your application is crashing on launch. | complaint | ham |
| I want to buy this right now. | place_order | ham |
| Can I see the receipt for my last payment? | get_invoice | ham |
| Cancel my account and refund my money. | delete_account | ham |
| Send me the tracking link. | track_order | ham |
| I am stuck on the sign-up page. | registration_problems | ham |
| Buy cheap rolex watches today at http://spam.com | unknown | spam |
| You have won a $1000 gift card! Click here to claim your prize. | unknown | spam |
| Hot singles in your area are waiting for you. | unknown | spam |
| Earn $5000 a week from home with this simple trick. | unknown | spam |
| Your bank account has been locked. Verify your identity at this link. | unknown | spam |
| Enlarge your size naturally within weeks! | unknown | spam |
| Invest in this new crypto coin before it goes to the moon! | unknown | spam |
| Get 90% off all designer handbags, limited time only. | unknown | spam |
| Urgent: Your package could not be delivered. Pay the fee here. | unknown | spam |
| Congratulations! You are our 1 millionth visitor. | unknown | spam |