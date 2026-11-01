# BH-OMNI CORE

BH-OMNI CORE is an experimental, modular Python brain foundation. It currently includes:

- JSON-based shared knowledge storage and keyword search.
- Per-user JSON memory storage.
- A word-level tokenizer with a persistent vocabulary.
- A small feed-forward sigmoid neural network for numeric learning experiments.
- Deterministic text feature extraction and a small text-classification network.
- A network registry with activation, priorities, directed connection metadata, and independent network execution.
- A keyword-based prediction cache.

## Requirements

- Python 3.10 or newer
- No third-party Python packages are required.

## Run tests

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m brain.test_brain
python -m brain.test_brain_core
python -m brain.health_check
```

## Important limitations

This is not a large language model and does not generate fluent natural-language answers. Knowledge search is keyword-based. The tokenizer is word-level, not BPE or SentencePiece. The neural network is a small numerical feed-forward network, not a transformer. Network connections currently store directed relationships; they do not automatically pass outputs between connected networks. User memory files are separated by a hash of the supplied user ID, but this is not authentication, encryption, or a security boundary. Do not store sensitive personal information in this prototype.

The project is a foundation for further development, not a trained general-purpose AI.
