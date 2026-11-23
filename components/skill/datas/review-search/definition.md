# Individual buyer reviews for an ASIN

Use individual reviews when the question asks for buyers’ original words or evidence of a particular concern. Reuse supplied reviews when they cover the requested sample.

## Task input

One product ASIN and the requested review selection.

## Endpoints and call order

Use the connected operation `openapi_v2_reviews_search` for `reviews/search`. Check its schema on first use. Each page costs 1 credit.

## `reviews/search`

### Request parameters

| Inputs | How to select them |
|---|---|
| `asin` | Required. One ASIN selects its parent's reviews. |
| `dateStart`, `dateEnd`, `ratingMin`, `ratingMax` | Inclusive review dates in YYYY-MM-DD and inclusive star bounds. |
| `verifiedOnly`, `vineOnly`, `helpfulVoteCountMin`, `mediaTypes` | Combine requested filters with AND. For reviews with images use ["image"]. Tags can be read from results but cannot be sent as filters. |
| `sortBy`, `sortOrder` | Default is `recent` descending. Select `rating` or `helpfulVoteCount` when requested. Directions are `asc` and `desc`. |
| `page`, `pageSize` | Start at 1. Default 10 reviews per page, maximum 20. Read further pages only for the requested coverage and budget. |

Example for five low-star reviews, newest first:

```json
{"asin":"B000000001","ratingMax":2,"pageSize":5}
```

### Response handling

1. Return relevant excerpts, review IDs, dates, stars and known variants. Treat reviews as belonging to the parent. Attribute feedback to a particular variant only when the record identifies it.
2. State which reviews were examined when counting mentions. The search considers at most 5,000 reviews per parent before filtering, so the reported total can be capped.
3. Zero matches means no reviews met the selected conditions. Keep those conditions and avoid repeating a billed page. If the connector is unavailable, identify the missing coverage.

## Deliverable

Review text with available dates, stars and variants.
