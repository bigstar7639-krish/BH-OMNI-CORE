
# BH-OMNI CORE

BH-OMNI CORE is an experimental, modular Python brain foundation. It is designed as a starting point for building and testing independent AI-related components.

## Current Features

- JSON-based shared knowledge storage and keyword search.
- Per-user JSON memory storage.
- A word-level tokenizer with a persistent vocabulary.
- A small feed-forward sigmoid neural network for numerical learning experiments.
- Deterministic text feature extraction.
- A small text-classification network.
- A network registry with activation controls, priorities, directed connection metadata, and independent network execution.
- A keyword-based prediction cache.
- Automated unit tests and basic health checks.

## Requirements

- Python 3.10 or newer.
- No third-party Python packages are required.

## Run Tests

Run these commands from the repository root:

```bash
python -m unittest discover -s tests -v
python -m brain.test_brain
python -m unittest brain.test_brain_core -v
python -m brain.health_check
```

## Project Structure

```text
BH-OMNI-CORE/
├── brain/
├── tests/
├── .github/
│   └── workflows/
└── README.md
```

## Important Limitations

- This project is not a large language model and does not generate fluent, general-purpose natural-language answers.
- Knowledge search is keyword-based.
- The tokenizer is word-level, not BPE or SentencePiece.
- The neural network is a small numerical feed-forward network, not a transformer.
- Network connections currently store directed relationships; they do not automatically pass outputs between connected networks.
- User memory files are separated using a hash of the supplied user ID. This is not authentication, encryption, or a security boundary.
- Do not store sensitive personal information in this prototype.

## Project Status

BH-OMNI CORE is an experimental foundation for further development. Its components are modular and testable, but it is not yet a trained general-purpose AI system.
