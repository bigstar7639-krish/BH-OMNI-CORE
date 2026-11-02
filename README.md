
# BH-OMNI CORE

BH-OMNI CORE is an experimental, modular Python AI foundation. It provides independent components for text processing, numerical feature storage, knowledge retrieval, memory, and small neural-network experiments.

## Current Features

- JSON-based shared knowledge storage and keyword search.
- Per-user JSON memory storage.
- Word-level tokenizer with persistent vocabulary.
- Small feed-forward sigmoid neural network.
- Deterministic numerical text feature extraction.
- Text classification network.
- Network registry with activation controls, priorities, and directed connection metadata.
- Keyword-based prediction cache.
- Unicode-aware lexical text relevance ranking.
- Script analysis for supported writing systems.
- Multilingual text-processing pipeline.
- Batch processing for multiple text inputs.
- Sparse numerical feature operations.
- Dynamically allocated numerical feature IDs.
- Feature registry with persistent IDs and JSON storage.
- Automated unit tests and health checks.

## Requirements

- Python 3.10 or newer.
- No third-party Python packages required.

## Run Tests

Run from the repository root:

```bash
python -m compileall -q brain tests
python -m unittest discover -s tests -v
python -m brain.test_brain
python -m unittest brain.test_brain_core -v
python -m brain.health_check
python -m brain.multilingual_health_check
```

## Project Structure

```text
BH-OMNI-CORE/
├── brain/
│   ├── brain_core.py
│   ├── feature_registry.py
│   ├── language_analyzer.py
│   ├── multilingual_pipeline.py
│   ├── numeric_brain.py
│   ├── text_relevance_engine.py
│   └── ...
├── tests/
├── .github/
│   └── workflows/
└── README.md
```

## Important Limitations

- This project is not a large language model.
- It does not currently provide ChatGPT-level natural-language understanding or generation.
- Text relevance uses lexical similarity, not deep semantic understanding.
- Script detection is not the same as language identification or translation.
- The tokenizer is word-level, not BPE or SentencePiece.
- The neural network is a small numerical feed-forward network, not a transformer.
- Network connections store directed relationships; they do not automatically transfer outputs between networks.
- Dynamic numerical feature IDs do not mean unlimited physical storage. Available memory and storage remain finite.
- User memory filenames are hashed, but this is not authentication or encryption.
- Do not store sensitive personal information in this prototype.

## Project Status

BH-OMNI CORE is an experimental foundation for further development. Its components are modular and testable, but it is not yet a trained general-purpose AI system.
