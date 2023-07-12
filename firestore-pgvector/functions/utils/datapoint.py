from dataclasses import dataclass
from typing import Optional
import numpy as np



@dataclass
class Datapoint:
    id: str
    content: str
    embedding: Optional[np.array] = None