# Minifying Tables with `pymtd2json`: Boosting Efficiency in RAG Systems

In retrieval-augmented generation (RAG) pipelines, input efficiency is paramount — not just in terms of tokens, but also **character limits**.  

When building a multilingual embedding pipeline, I faced a real challenge:  
the Cohere multilingual model imposes a **maximum of 2048 characters**, not a token limit per input.

This article walks you through a clever solution:  
**preprocessing Markdown tables into dense JSON blocks** using `pymtd2json`, to ensure smooth, efficient embeddings without errors.


## The Challenge: Character Limits vs Token Limits

Classical chunking methods, like `SentenceSplitter` from LlamaIndex, are token-focused:  
you set a maximum number of tokens per chunk — but **not characters**.

### Why This Matters:

- Markdown (especially GitHub-Flavored Markdown, GFM) **wastes space** with formatting.
- A Markdown chunk might have only 170 tokens but **still exceed 2048 characters**.
- This results in **rejected API requests** or **inefficient extra splitting**.

**Important Note**:  
Markdown tables are up to **3x less token-efficient** than other formats, further compounding the problem.  
👉 [Read more on token inefficiency of Markdown tables here.](https://medium.com/singapore-gds/cutting-cost-and-enhancing-performance-minifying-markdown-tables-to-improve-token-efficiency-in-af488a784fd5)


## A Real-World Example: Measuring the Problem

Let's dive into a simple simulation:

### Step 1: Create a Large Markdown Table

```python
import pandas as pd

# Build data
data = {
    "Name": [f"Person{i}" for i in range(30)],
    "Age": [20 + i for i in range(30)],
    "City": [f"City{i}" for i in range(30)]
}

# Create DataFrame
df = pd.DataFrame(data)
df.columns = ["A very long row content, which leads to a lot of white spaces", "Age", "City"]

# Convert to Markdown
table_text = df.to_markdown(index=False)
print(table_text)
```

This generates a verbose table with **30 rows** and a **very long header**.


### Step 2: Analyze Token and Character Counts

Using Cohere’s tokenizer (available via Hugging Face):

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Cohere/Cohere-embed-multilingual-v3.0")
encoded = tokenizer(table_text, return_tensors="pt", add_special_tokens=False)

num_tokens = encoded.input_ids.shape[-1]
num_chars = len(table_text)

print(f"Characters: {num_chars}")
print(f"Tokens: {num_tokens}")
```

**Result:**

- Characters: **2719**
- Tokens: **432**

⚡ **Problem**:  
While token count is fine, character count **exceeds 2048**, causing API errors like:

```
cohere.error.CohereAPIError: input text exceeds maximum allowed size of 2048 characters
```


## The Solution: Minifying Tables into JSON

Instead of traditional Markdown, why not store the data in a **dense JSON block**?

### Benefits of Minifying Tables:

- Remove **pipes, dashes, and whitespace** — all formatting overhead.
- Preserve **semantic meaning**.
- Shrink text to meet character limits safely.

Example of the compact JSON:

```json
{"Name":["Person0","Person1","Person2",...],"Age":["20","21","22",...],"City":["City0","City1","City2",...]}
```

**New Stats:**

- Characters: **1027**
- Tokens: **461**

✅ Now **well within** Cohere’s input limit!


## Applying Minification in Practice

Want to prepare documents before chunking?  
Here's how you can automatically process all Markdown files:

```python
from pathlib import Path
from llama_index import SimpleDirectoryReader
from your_minifier import MinifyMDT

source_dir = Path("example_dir", "markdown")

documents = SimpleDirectoryReader(source_dir, required_exts=[".md"], recursive=True).load_data()

doc_texts = []
for idx, doc in enumerate(documents):
    doc_texts.append(MinifyMDT(doc.text_resource.text).transform())
```

👉 And voilà: **Your data is compact, clean, and embedding-ready!**


# Final Thoughts

Working with multilingual RAG systems means **optimizing every byte**.  
Whitespace-heavy Markdown tables might look nice for humans, but they’re **expensive** for machine understanding.

By minifying your tables with `pymtd2json`, you:

- Cut down API errors.
- Reduce token overhead.
- Boost overall performance.

**Efficiency isn't optional — it's a superpower.** 🚀