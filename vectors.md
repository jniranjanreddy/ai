## Vector database..
```
What are embeddings in AI? (plain English)

An embedding is a way to convert text, images, audio, or any data into a list of numbers (a vector) so that:

Similar things → vectors close to each other

Different things → vectors far apart

Think of embeddings as meaning in numbers.

Example idea:

“dog” 🐶 and “puppy” → vectors very close

“dog” and “car” 🚗 → vectors far apart

Simple intuition (non-AI analogy)

Imagine a map:

Cities that are close = similar

Cities far apart = different

Embeddings create a map of meaning in high-dimensional space (128, 384, 768, 1536 dimensions, etc.).

Text embedding example (human view)

Sentences:

"I love Azure cloud"

"Azure is my favorite cloud platform"

"I enjoy playing cricket"

After embedding (fake simplified vectors):

"I love Azure cloud"                → [0.12, 0.98, 0.33, ...]
"Azure is my favorite cloud platform" → [0.11, 0.97, 0.34, ...]
"I enjoy playing cricket"           → [0.88, 0.02, 0.71, ...]


👉 1 & 2 are close
👉 3 is far away

Why embeddings are used with Milvus
Milvus is a vector database, so it stores:

🔢 Embeddings (vectors)
🏷 Metadata (text, ids, tags, timestamps, etc.)
Typical use cases:
Semantic search
RAG (Retrieval Augmented Generation)
Chatbots
Recommendation systems
Similarity search

```
## example
```
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Azure cloud architecture",
    "AWS cloud services",
    "Playing cricket on Sunday"
]

embeddings = model.encode(sentences)

print(len(embeddings))      # 3
print(len(embeddings[0]))   # 384

```
