
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
- Experimental rule-based semantic feature extraction.
- Automated unit tests and health checks.

## Requirements

- Python 3.10 or newer.
- No third-party Python packages required.

## Run Tests

Run these commands from the repository root:

```bash
python -m compileall -q brain tests
python -m unittest discover -s tests -v
python -m brain.test_brain
python -m brain.health_check
python -m brain.multilingual_health_check
python -m brain.semantic_health_check
```

## GitHub Actions

Automated tests run through GitHub Actions on:

- Pushes to the `main` branch.
- Pull requests targeting `main`.
- Manual workflow dispatch.

Workflow file:

```text
.github/workflows/brain-tests.yml
```

## Project Structure

```text
BH-OMNI-CORE/
├── brain/
│   ├── brain_core.py
│   ├── feature_registry.py
│   ├── language_analyzer.py
│   ├── multilingual_pipeline.py
│   ├── multilingual_numeric_bridge.py
│   ├── semantic_feature_engine.py
│   ├── semantic_health_check.py
│   ├── numeric_brain.py
│   ├── text_feature_engine.py
│   ├── text_relevance_engine.py
│   └── ...
├── tests/
├── .github/
│   └── workflows/
└── README.md
```

## Semantic Feature Engine

BH-OMNI CORE includes an experimental rule-based semantic feature engine.

### Current Features

- Basic positive and negative sentiment signals.
- English and selected Tamil negation detection.
- Basic urgency detection.
- Basic question detection.
- Sentence boundary handling.
- Unicode normalization.
- Tamil and English mixed-text support.

### Output Signals

- `question_signal`
- `negation_signal`
- `sentiment_signal`
- `urgency_signal`
- `token_count`

### Current Limitations

- Uses predefined word lists, not a trained language model.
- Does not understand every language or sentence structure.
- Negation handling is limited to nearby words.
- Does not provide reliable translation or deep contextual understanding.

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
