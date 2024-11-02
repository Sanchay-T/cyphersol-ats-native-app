import os
import warnings
from gliner import GLiNER

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load model ONCE
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# List of texts to process
texts = [
    "John works at Microsoft in Seattle",
    "Sarah joined Apple Inc last year",
    "Google's CEO Sundar Pichai announced...",
    # ... more texts ...
]

labels = ["person", "organization", "location"]

# Process all texts efficiently
results = []
for text in texts:
    entities = model.predict_entities(text, labels)
    results.append(entities)

# Print results
for i, entities in enumerate(results):
    print(f"\nText {i+1} entities:")
    for entity in entities:
        print(f"{entity['text']} => {entity['label']}")