## Try it out

Once processing is complete, a Callable function will be available to the user to use for queries. Queries are just a string that will be matched against all data in the Index.

Call the HTTPS function `queryindex` (TODO: add actual endpoint/change to callable) deployed by the extension with a POST request.

Sample request body:

```json
{
  "query": "mens jacket",
  "limit": 3
}
```

Sample response:

```json
[
  {
    "EkH4WCdb2p38ApFxmcZW": "Mens Cotton Jacket",
    "rehUqqDW9zTsgmH1kVOe": "Mens Casual Slim Fit",
    "xcO1EYsrorrT6TAj8CNM": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats"
  }
]

```