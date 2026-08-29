# Training data expected by MDAS

Place these four CSV files here:

## spam.csv
Columns: `text`, `label`. Expected UCI-style labels: `ham`, `spam`.

## sentiment.csv
Columns: `text`, `label`. The existing MTAS notebook used Twitter US Airline Sentiment with `negative`, `neutral`, `positive` labels.

## intent.csv
Columns: `text`, `label`. The existing MTAS notebook used Bitext Customer Support intent data.

## category.csv
Columns: `text`, `label`. The existing MTAS notebook used CFPB consumer complaint product categories.

Keep dataset URLs, licenses/terms, exact versions, row counts, class counts and split seed in your project report. The code intentionally does not pretend these datasets are a universal English corpus.

## moderation.csv
Columns: `text`, `label`. Recommended V1 labels: `Safe`, `Hate Speech`, `Harassment`, `Violence`. Use a documented annotation policy.

## document_type.csv
Columns: `text`, `label`. Define your project taxonomy first (for example `Complaint`, `Request`, `Question`, `Feedback`, `Other`) and label consistently.
