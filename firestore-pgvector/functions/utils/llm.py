from vertexai.preview.language_models import TextEmbeddingModel
from typing import List
from utils.datapoint import Datapoint
import numpy as np

model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

def assign_embeddings(datapoints: List[Datapoint]) -> List[Datapoint]:
    """Text embedding with a Large Language Model, limited to 5 at a time"""

    if (len(datapoints) > 5):
        raise Exception("Too many datapoints, PaLM only allows 5 embeddings at a time.")

    inputs = [d.content for d in datapoints]
    embeddings = model.get_embeddings(inputs)

    for i, embedding in enumerate(embeddings):
        datapoints[i].embedding = np.array(embedding.values)

    return datapoints