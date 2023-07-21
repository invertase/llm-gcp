> ⚠️ The PaLM API is currently in public preview.
>
> For details and limitations, see the (documentation reference)
>

This extension adds text similarity search to your Firestore application using `pgvector` and Cloud SQL. Text similarity search relies on first generating embeddings (vector representations of your original text) which are stored in a postgresql table. Once these embeddings are uploaded to Cloud SQL, `pgvector` can be used to calculate semantically similar documents to an original document from a large corpus of candidate documents, based on vector distance measures.

On installation, you will need to specify a Firestore collection path to index and the document fields to index, as well as information about your Cloud SQL instance.

Once installed, the extension does the following:

1. Automatically generates and stores embeddings in your Cloud SQL PostgreSQL whenever documents are created, updated, or deleted in the target collection.
2. Provides an API endpoint to query similar documents (given an input document) that can be used by client applications
3. (Optional) Backfills existing data from target collection(s)

The query API endpoint is deployed as a Firebase HTTPS Function.

## Additional Setup

### PaLM API access (optional)

If you would like to use the PaLM embeddings model, you will first need to apply for access to the PaLM API via this [waitlist](https://makersuite.google.com/waitlist).

### Cloud Firestore and Cloud Storage setup

Make sure that you've set up a [Cloud Firestore database](https://firebase.google.com/docs/firestore/quickstart) and [enabled Cloud Storage](https://firebase.google.com/docs/storage) in your Firebase project.

After installation, you will need to also add some security rules on a new Firestore collection created by the extension that is used to store internal backfill state. Please check the extension instance after installation for more details.

### Installation time

## Billing

To install an extension, your project must be on the Blaze (pay as you go) plan. You will be charged a small amount (typically around $0.01/month) for the Firebase resources required by this extension (even if it is not used).
This extension uses other Firebase and Google Cloud Platform services, which have associated charges if you exceed the service's no-cost tier:

- Cloud Firestore
- Cloud Storage
- Cloud Run
- Cloud EventArc
- [Vertex AI](https://cloud.google.com/vertex-ai/pricing)
- Cloud Functions (See [FAQs](https://firebase.google.com/support/faq#extensions-pricing))

[Learn more about Firebase billing](https://firebase.google.com/pricing).

Additionally, this extension uses the PaLM API, which is currently in public preview. During the preview period, developers can try the PaLM API at no cost. Pricing will be announced closer to general availability. For more information on the PaLM API public preview, see the [PaLM API documentation](https://developers.generativeai.google/guide/preview_faq).

> :warning: Note: The extension does not delete the Matching Engine Index automatically when you uninstall the extension.
>
> Vertex AI charges by node hour when hosting a Matching Engine Index, so your project will continue to incur costs until you manually undeploy the index. Instructions for undeploying an index are available [here](https://cloud.google.com/vertex-ai/docs/matching-engine/deploy-index-public#undeploy-index).
>
> You can [read more about Matching Engine pricing here](https://www.google.com/url?q=https://cloud.google.com/vertex-ai/pricing%23matchingengine&sa=D&source=docs&ust=1683194254385742&usg=AOvVaw1kYFVKa8gdagrau70Vzk6G).