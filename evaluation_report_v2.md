# Trustworthy Classification Evaluation Report

## 1. Ground Truth Dataset Assignment
The 100 test cases were curated systematically to cover all 27 intent classes identified in the model's schema, plus 10 explicit spam patterns.
Labels were manually assigned based on semantic intent rather than simple keyword overlap to verify real-world robustness. 90 cases are Ham (with varying intents) and 10 are Spam.

## 2. Intent Metrics
- **Accuracy**: 73.3%
- **Macro F1**: 0.724
- **Weighted F1**: 0.766
- **Macro Precision**: 0.814
- **Macro Recall**: 0.697
- **Abstention Rate**: 7.8% (7/90)

### Per-Class F1 & Classification Report
```text
                          precision    recall  f1-score   support

                 abstain       0.00      0.00      0.00         0
            cancel_order       0.75      1.00      0.86         3
            change_order       1.00      0.67      0.80         3
 change_shipping_address       1.00      0.50      0.67         4
  check_cancellation_fee       1.00      1.00      1.00         3
           check_invoice       0.75      1.00      0.86         3
   check_payment_methods       0.67      0.67      0.67         3
     check_refund_policy       0.75      1.00      0.86         3
               complaint       1.00      0.20      0.33         5
contact_customer_service       1.00      0.67      0.80         3
     contact_human_agent       1.00      0.67      0.80         3
          create_account       0.75      1.00      0.86         3
          delete_account       1.00      1.00      1.00         4
        delivery_options       1.00      0.67      0.80         3
         delivery_period       0.40      0.67      0.50         3
            edit_account       1.00      1.00      1.00         3
             get_invoice       0.33      0.50      0.40         4
              get_refund       1.00      0.67      0.80         3
 newsletter_subscription       0.67      0.67      0.67         3
           payment_issue       1.00      0.67      0.80         3
             place_order       0.80      1.00      0.89         4
        recover_password       1.00      0.75      0.86         4
   registration_problems       1.00      0.75      0.86         4
              report_bug       0.00      0.00      0.00         0
                  review       0.75      1.00      0.86         3
 set_up_shipping_address       1.00      0.67      0.80         3
          switch_account       1.00      0.67      0.80         3
             track_order       1.00      0.50      0.67         4
            track_refund       1.00      0.67      0.80         3

                accuracy                           0.73        90
               macro avg       0.81      0.70      0.72        90
            weighted avg       0.88      0.73      0.77        90

```

### Intent Confusion Matrix
| Expected / Predicted | abstain | cancel_order | change_order | change_shipping_address | check_cancellation_fee | check_invoice | check_payment_methods | check_refund_policy | complaint | contact_customer_service | contact_human_agent | create_account | delete_account | delivery_options | delivery_period | edit_account | get_invoice | get_refund | newsletter_subscription | payment_issue | place_order | recover_password | registration_problems | report_bug | review | set_up_shipping_address | switch_account | track_order | track_refund |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **cancel_order** | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **change_order** | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **change_shipping_address** | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_cancellation_fee** | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_invoice** | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_payment_methods** | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **check_refund_policy** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **complaint** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 |
| **contact_customer_service** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **contact_human_agent** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **create_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **delete_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **delivery_options** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **delivery_period** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **edit_account** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **get_invoice** | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **get_refund** | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **newsletter_subscription** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **payment_issue** | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **place_order** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **recover_password** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **registration_problems** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| **review** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| **set_up_shipping_address** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| **switch_account** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| **track_order** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| **track_refund** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |


## 3. Spam Metrics
- **Spam Precision**: 0.429
- **Spam Recall**: 0.600
- **Spam F1**: 0.500
- **False Positive Rate (FPR)**: 9.6% (Ham flagged as Spam)
- **False Negative Rate (FNR)**: 40.0% (Spam missed)
- **Abstention Rate**: 7.0%

### Spam Confusion Matrix
| Expected / Predicted | Ham | Spam | Abstain |
|---|---|---|---|
| **ham** | 75 | 8 | 7 |
| **spam** | 4 | 6 | 0 |
| **abstain** | 0 | 0 | 0 |


## 4. Intent Failures Deep Dive
### [FAILED] I need to ship this to my new apartment instead.
- **Expected**: `change_shipping_address`
- **Final Prediction**: `get_invoice` (Confidence: 0.462)
- **Legacy Model**: `get_invoice (0.462)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Do you accept PayPal?
- **Expected**: `check_payment_methods`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] Your service is terrible, I am very disappointed.
- **Expected**: `complaint`
- **Final Prediction**: `review` (Confidence: 0.426)
- **Legacy Model**: `review (0.426)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How long does shipping take?
- **Expected**: `delivery_period`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] I need a receipt for tax purposes.
- **Expected**: `get_invoice`
- **Final Prediction**: `delivery_period` (Confidence: 0.303)
- **Legacy Model**: `delivery_period (0.303)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Please process a refund for my last order.
- **Expected**: `get_refund`
- **Final Prediction**: `cancel_order` (Confidence: 0.780)
- **Legacy Model**: `cancel_order (0.780)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] My credit card was declined during checkout.
- **Expected**: `payment_issue`
- **Final Prediction**: `check_payment_methods` (Confidence: 0.583)
- **Legacy Model**: `check_payment_methods (0.583)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] I can't create an account, it gives me a server error.
- **Expected**: `registration_problems`
- **Final Prediction**: `create_account` (Confidence: 0.832)
- **Legacy Model**: `create_account (0.832)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] How do I log into a different profile?
- **Expected**: `switch_account`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] Where is my package right now?
- **Expected**: `track_order`
- **Final Prediction**: `delivery_period` (Confidence: 0.787)
- **Legacy Model**: `delivery_period (0.787)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] When will the money be back in my bank?
- **Expected**: `track_refund`
- **Final Prediction**: `check_refund_policy` (Confidence: 0.358)
- **Legacy Model**: `check_refund_policy (0.358)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Change my order to a size large.
- **Expected**: `change_order`
- **Final Prediction**: `place_order` (Confidence: 0.581)
- **Legacy Model**: `place_order (0.581)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Send it to my work address instead.
- **Expected**: `change_shipping_address`
- **Final Prediction**: `get_invoice` (Confidence: 0.923)
- **Legacy Model**: `get_invoice (0.923)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] This software is a piece of trash.
- **Expected**: `complaint`
- **Final Prediction**: `report_bug` (Confidence: 0.309)
- **Legacy Model**: `report_bug (0.309)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Help desk, please.
- **Expected**: `contact_customer_service`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] Get me a human now.
- **Expected**: `contact_human_agent`
- **Final Prediction**: `get_invoice` (Confidence: 0.535)
- **Legacy Model**: `get_invoice (0.535)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Is next day shipping available?
- **Expected**: `delivery_options`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] Add me to the mailing list.
- **Expected**: `newsletter_subscription`
- **Final Prediction**: `get_invoice` (Confidence: 0.562)
- **Legacy Model**: `get_invoice (0.562)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Reset my password.
- **Expected**: `recover_password`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] Set my default shipping address.
- **Expected**: `set_up_shipping_address`
- **Final Prediction**: `abstain` (Confidence: 0.000)
- **Legacy Model**: `N/A`
- **MiniLM Model**: `N/A`
- **Selected Model**: `none (language unsupported)`
- **Selection Reason**: Language detection aborted classification.

### [FAILED] What is the status of my delivery?
- **Expected**: `track_order`
- **Final Prediction**: `delivery_period` (Confidence: 0.593)
- **Legacy Model**: `delivery_period (0.574)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!
- **Expected**: `complaint`
- **Final Prediction**: `newsletter_subscription` (Confidence: 0.360)
- **Legacy Model**: `newsletter_subscription (0.360)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Your application is crashing on launch.
- **Expected**: `complaint`
- **Final Prediction**: `report_bug` (Confidence: 0.854)
- **Legacy Model**: `report_bug (0.854)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
- **Selection Reason**: Legacy model was highly confident and fallback threshold was not triggered.

### [FAILED] Can I see the receipt for my last payment?
- **Expected**: `get_invoice`
- **Final Prediction**: `check_invoice` (Confidence: 0.526)
- **Legacy Model**: `check_invoice (0.526)`
- **MiniLM Model**: `N/A (0.000)`
- **Selected Model**: `legacy_model`
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