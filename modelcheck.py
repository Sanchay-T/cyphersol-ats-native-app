from gliner import GLiNER
import os
import warnings
# Load the model

# Suppress all warnings
warnings.filterwarnings('ignore')
# Disable symlinks warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# Basic usage
text = """
upi/312465553183/jimmy/allsaintsgohell/axisbankltd./axi6b0c56a10ccc41718a3ce6
"""
labels = ["person", "organization", "location"]

# Just use the basic parameters
entities = model.predict_entities(text, labels)

# Add a confidence threshold
filtered_entities = [
    entity for entity in entities 
    if entity['score'] > 0.5  # Adjust threshold as needed
]

# Print results with confidence scores
for entity in filtered_entities:
    print(f"{entity['text']} => {entity['label']} (confidence: {entity['score']:.2f})")