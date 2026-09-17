# Category selection workflow

## Data-Driven Category Selection (no specific category given)
Scan with `market --scope subtree --sales-min 200 --page-size 20` under a stated page/credit budget; do not paginate the entire global catalog by default. Rank observed category markets by `totalMonthlySales`, `top100ConservativeNewProductRate6m`, `top100FbmRate`, and `top100MedianPrice`. Treat Top 100 fields as selected-sample evidence and label the ranking as limited to scanned pages. Pick top 3-5; use their returned `categoryId` for deeper evidence.
