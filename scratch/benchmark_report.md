# Phase 1: Dataset & Benchmark Report

## Dataset Audit

### SPAM
- **Rows**: 200
- **Classes**: 2
- **Minimum Class Count**: 100
- **Distribution**: ham: 100, spam: 100
- **Status**: ✅ viable (Reason: None)

### SENTIMENT
- **Rows**: 300
- **Classes**: 3
- **Minimum Class Count**: 100
- **Distribution**: negative: 100, neutral: 100, positive: 100
- **Status**: ✅ viable (Reason: None)

### INTENT
- **Status**: ERROR
- **Reason**: Cannot take a larger sample than population when 'replace=False'

### CATEGORY
- **Status**: ERROR
- **Reason**: Cannot take a larger sample than population when 'replace=False'

### MODERATION
- **Status**: ERROR
- **Reason**: data\raw\moderation.csv requires columns 'text' and 'label'

### DOCUMENT_TYPE
- **Status**: ERROR
- **Reason**: data\raw\document_type.csv requires columns 'text' and 'label'

### SARCASM
- **Rows**: 181
- **Classes**: 2
- **Minimum Class Count**: 90
- **Distribution**: genuine: 91, sarcastic: 90
- **Status**: ✅ viable (Reason: None)

---

## Benchmark Results (Viable Tasks)

### Task: SPAM

| Rank | Candidate | Macro F1 | Weighted F1 | Accuracy | Latency/Sample | CV Time (5 folds) |
|------|-----------|----------|-------------|----------|----------------|-------------------|
| 1 🏆 | minilm + LogisticRegression | **0.9548** | 0.9548 | 0.9548 | 0.02566s | 25.66s |
| 2  | minilm + LinearSVC | **0.9498** | 0.9498 | 0.9498 | 0.02656s | 26.56s |
| 3  | char_tfidf + LogisticRegression | **0.9297** | 0.9297 | 0.9298 | 0.00014s | 0.14s |
| 4  | char_tfidf + LinearSVC | **0.9296** | 0.9296 | 0.9297 | 0.00015s | 0.15s |
| 5  | char_tfidf + MultinomialNB | **0.9249** | 0.9249 | 0.9249 | 0.00016s | 0.16s |
| 6  | minilm + RandomForest | **0.915** | 0.915 | 0.9152 | 0.02774s | 27.74s |
| 7  | minilm + SGDClassifier | **0.9045** | 0.9044 | 0.9049 | 0.02608s | 26.08s |
| 8  | char_tfidf + SGDClassifier | **0.8995** | 0.8995 | 0.8999 | 0.00015s | 0.15s |
| 9  | word_tfidf + LinearSVC | **0.8797** | 0.8797 | 0.8798 | 0.00004s | 0.04s |
| 10  | word_tfidf + MultinomialNB | **0.8797** | 0.8796 | 0.8798 | 0.00005s | 0.05s |
| 11  | word_tfidf + LogisticRegression | **0.8746** | 0.8745 | 0.8748 | 0.00005s | 0.05s |
| 12  | char_tfidf + RandomForest | **0.8743** | 0.8743 | 0.875 | 0.00031s | 0.31s |
| 13  | word_tfidf + RandomForest | **0.8584** | 0.8584 | 0.8597 | 0.00022s | 0.22s |
| 14  | word_tfidf + SGDClassifier | **0.8188** | 0.8187 | 0.8198 | 0.00004s | 0.04s |

### Task: SENTIMENT

| Rank | Candidate | Macro F1 | Weighted F1 | Accuracy | Latency/Sample | CV Time (5 folds) |
|------|-----------|----------|-------------|----------|----------------|-------------------|
| 1 🏆 | minilm + LinearSVC | **0.7196** | 0.7193 | 0.72 | 0.01672s | 25.08s |
| 2  | minilm + SGDClassifier | **0.6879** | 0.6879 | 0.69 | 0.01471s | 22.06s |
| 3  | minilm + LogisticRegression | **0.6802** | 0.68 | 0.6833 | 0.01582s | 23.73s |
| 4  | char_tfidf + LinearSVC | **0.6125** | 0.612 | 0.6133 | 0.00014s | 0.21s |
| 5  | char_tfidf + LogisticRegression | **0.5794** | 0.579 | 0.5833 | 0.00025s | 0.37s |
| 6  | char_tfidf + SGDClassifier | **0.578** | 0.5778 | 0.58 | 0.00013s | 0.2s |
| 7  | word_tfidf + LinearSVC | **0.5762** | 0.5761 | 0.5767 | 0.00004s | 0.07s |
| 8  | word_tfidf + LogisticRegression | **0.5753** | 0.5749 | 0.5767 | 0.00006s | 0.09s |
| 9  | minilm + RandomForest | **0.5673** | 0.5669 | 0.5767 | 0.01357s | 20.36s |
| 10  | word_tfidf + MultinomialNB | **0.5568** | 0.5567 | 0.5567 | 0.00003s | 0.05s |
| 11  | word_tfidf + SGDClassifier | **0.5312** | 0.531 | 0.5333 | 0.00004s | 0.06s |
| 12  | char_tfidf + RandomForest | **0.5286** | 0.5282 | 0.53 | 0.00025s | 0.38s |
| 13  | char_tfidf + MultinomialNB | **0.5239** | 0.5232 | 0.5333 | 0.00012s | 0.18s |
| 14  | word_tfidf + RandomForest | **0.5142** | 0.5141 | 0.5167 | 0.00016s | 0.24s |

### Task: SARCASM

| Rank | Candidate | Macro F1 | Weighted F1 | Accuracy | Latency/Sample | CV Time (5 folds) |
|------|-----------|----------|-------------|----------|----------------|-------------------|
| 1 🏆 | word_tfidf + LogisticRegression | **1.0** | 1.0 | 1.0 | 0.00005s | 0.04s |
| 2  | word_tfidf + SGDClassifier | **1.0** | 1.0 | 1.0 | 0.00003s | 0.03s |
| 3  | word_tfidf + MultinomialNB | **1.0** | 1.0 | 1.0 | 0.00003s | 0.03s |
| 4  | word_tfidf + RandomForest | **1.0** | 1.0 | 1.0 | 0.00026s | 0.23s |
| 5  | word_tfidf + LinearSVC | **0.9944** | 0.9944 | 0.9944 | 0.00003s | 0.03s |
| 6  | char_tfidf + LogisticRegression | **0.9944** | 0.9944 | 0.9944 | 0.00008s | 0.07s |
| 7  | char_tfidf + LinearSVC | **0.9944** | 0.9944 | 0.9944 | 0.00007s | 0.06s |
| 8  | char_tfidf + SGDClassifier | **0.9944** | 0.9944 | 0.9944 | 0.00008s | 0.07s |
| 9  | char_tfidf + MultinomialNB | **0.9944** | 0.9944 | 0.9944 | 0.00007s | 0.06s |
| 10  | char_tfidf + RandomForest | **0.9944** | 0.9944 | 0.9944 | 0.00027s | 0.24s |
| 11  | minilm + LogisticRegression | **0.9944** | 0.9944 | 0.9944 | 0.02146s | 19.42s |
| 12  | minilm + LinearSVC | **0.9944** | 0.9944 | 0.9944 | 0.01833s | 16.59s |
| 13  | minilm + SGDClassifier | **0.9944** | 0.9944 | 0.9944 | 0.02053s | 18.58s |
| 14  | minilm + RandomForest | **0.9944** | 0.9944 | 0.9944 | 0.02212s | 20.02s |

