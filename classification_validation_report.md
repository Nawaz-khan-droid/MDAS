# Classification Validation Report

## 1. Executive Summary
- **Spam Accuracy**: 81/93 (87.1%)
- **Intent Accuracy**: 66/83 (79.5%)

## 2. Intent Confusion Matrix
| Expected | Predicted | Count |
|----------|-----------|-------|
| cancel_order | cancel_order | 3 |
| change_order | change_order | 2 |
| change_order | place_order | 1 |
| change_shipping_address | get_invoice | 2 |
| change_shipping_address | change_shipping_address | 2 |
| check_cancellation_fee | check_cancellation_fee | 3 |
| check_invoice | check_invoice | 3 |
| check_payment_methods | check_payment_methods | 2 |
| check_refund_policy | check_refund_policy | 3 |
| complaint | complaint | 1 |
| complaint | review | 1 |
| complaint | report_bug | 2 |
| complaint | newsletter_subscription | 1 |
| contact_customer_service | contact_customer_service | 2 |
| contact_human_agent | contact_human_agent | 2 |
| contact_human_agent | get_invoice | 1 |
| create_account | create_account | 3 |
| delete_account | delete_account | 4 |
| delivery_options | delivery_options | 2 |
| delivery_period | delivery_period | 2 |
| edit_account | edit_account | 3 |
| get_invoice | get_invoice | 2 |
| get_invoice | delivery_period | 1 |
| get_invoice | check_invoice | 1 |
| get_refund | get_refund | 2 |
| get_refund | cancel_order | 1 |
| newsletter_subscription | newsletter_subscription | 2 |
| newsletter_subscription | get_invoice | 1 |
| payment_issue | check_payment_methods | 1 |
| payment_issue | payment_issue | 2 |
| place_order | place_order | 4 |
| recover_password | recover_password | 3 |
| registration_problems | registration_problems | 3 |
| registration_problems | create_account | 1 |
| review | review | 3 |
| set_up_shipping_address | set_up_shipping_address | 2 |
| switch_account | switch_account | 2 |
| track_order | delivery_period | 2 |
| track_order | track_order | 2 |
| track_refund | track_refund | 2 |
| track_refund | check_refund_policy | 1 |

## 3. Intent Failures & RCA
### Failed: 'I need to ship this to my new apartment instead.'
- **Expected**: `change_shipping_address`
- **Actual**: `get_invoice` (Confidence: 0.462)
- **Selected Model**: legacy_model
- **Legacy Candidate**: get_invoice (0.462)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Your service is terrible, I am very disappointed.'
- **Expected**: `complaint`
- **Actual**: `review` (Confidence: 0.426)
- **Selected Model**: legacy_model
- **Legacy Candidate**: review (0.426)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'I need a receipt for tax purposes.'
- **Expected**: `get_invoice`
- **Actual**: `delivery_period` (Confidence: 0.303)
- **Selected Model**: legacy_model
- **Legacy Candidate**: delivery_period (0.303)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Please process a refund for my last order.'
- **Expected**: `get_refund`
- **Actual**: `cancel_order` (Confidence: 0.780)
- **Selected Model**: legacy_model
- **Legacy Candidate**: cancel_order (0.780)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'My credit card was declined during checkout.'
- **Expected**: `payment_issue`
- **Actual**: `check_payment_methods` (Confidence: 0.583)
- **Selected Model**: legacy_model
- **Legacy Candidate**: check_payment_methods (0.583)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'I can't create an account, it gives me a server error.'
- **Expected**: `registration_problems`
- **Actual**: `create_account` (Confidence: 0.832)
- **Selected Model**: legacy_model
- **Legacy Candidate**: create_account (0.832)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Where is my package right now?'
- **Expected**: `track_order`
- **Actual**: `delivery_period` (Confidence: 0.787)
- **Selected Model**: legacy_model
- **Legacy Candidate**: delivery_period (0.787)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'When will the money be back in my bank?'
- **Expected**: `track_refund`
- **Actual**: `check_refund_policy` (Confidence: 0.358)
- **Selected Model**: legacy_model
- **Legacy Candidate**: check_refund_policy (0.358)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Change my order to a size large.'
- **Expected**: `change_order`
- **Actual**: `place_order` (Confidence: 0.581)
- **Selected Model**: legacy_model
- **Legacy Candidate**: place_order (0.581)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Send it to my work address instead.'
- **Expected**: `change_shipping_address`
- **Actual**: `get_invoice` (Confidence: 0.923)
- **Selected Model**: legacy_model
- **Legacy Candidate**: get_invoice (0.923)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'This software is a piece of trash.'
- **Expected**: `complaint`
- **Actual**: `report_bug` (Confidence: 0.309)
- **Selected Model**: legacy_model
- **Legacy Candidate**: report_bug (0.309)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Get me a human now.'
- **Expected**: `contact_human_agent`
- **Actual**: `get_invoice` (Confidence: 0.535)
- **Selected Model**: legacy_model
- **Legacy Candidate**: get_invoice (0.535)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Add me to the mailing list.'
- **Expected**: `newsletter_subscription`
- **Actual**: `get_invoice` (Confidence: 0.562)
- **Selected Model**: legacy_model
- **Legacy Candidate**: get_invoice (0.562)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'What is the status of my delivery?'
- **Expected**: `track_order`
- **Actual**: `delivery_period` (Confidence: 0.593)
- **Selected Model**: legacy_model
- **Legacy Candidate**: delivery_period (0.574)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!'
- **Expected**: `complaint`
- **Actual**: `newsletter_subscription` (Confidence: 0.360)
- **Selected Model**: legacy_model
- **Legacy Candidate**: newsletter_subscription (0.360)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Your application is crashing on launch.'
- **Expected**: `complaint`
- **Actual**: `report_bug` (Confidence: 0.854)
- **Selected Model**: legacy_model
- **Legacy Candidate**: report_bug (0.854)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

### Failed: 'Can I see the receipt for my last payment?'
- **Expected**: `get_invoice`
- **Actual**: `check_invoice` (Confidence: 0.526)
- **Selected Model**: legacy_model
- **Legacy Candidate**: check_invoice (0.526)
- **MiniLM Candidate**: N/A
> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.

## 4. Spam Failures
- **Text**: 'Please abort my recent purchase.'
  - Expected: ham, Actual: spam (0.532)
- **Text**: 'What credit cards can I use on your site?'
  - Expected: ham, Actual: spam (0.664)
- **Text**: 'Can someone from support please assist me?'
  - Expected: ham, Actual: spam (0.790)
- **Text**: 'I would like to register for your website.'
  - Expected: ham, Actual: spam (0.729)
- **Text**: 'What are the available shipping options?'
  - Expected: ham, Actual: spam (0.641)
- **Text**: 'I want to buy the premium package.'
  - Expected: ham, Actual: spam (0.669)
- **Text**: 'Please send a password reset link.'
  - Expected: ham, Actual: spam (0.517)
- **Text**: 'Cancel my account and refund my money.'
  - Expected: ham, Actual: spam (0.687)
- **Text**: 'Earn $5000 a week from home with this simple trick.'
  - Expected: spam, Actual: ham (0.675)
- **Text**: 'Enlarge your size naturally within weeks!'
  - Expected: spam, Actual: ham (0.971)
- **Text**: 'Get 90% off all designer handbags, limited time only.'
  - Expected: spam, Actual: ham (0.732)
- **Text**: 'Urgent: Your package could not be delivered. Pay the fee here.'
  - Expected: spam, Actual: ham (0.598)