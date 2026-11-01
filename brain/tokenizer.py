import re
import json
from pathlib import Path


class BHTokenizer:

    SPECIAL_TOKENS = [
        "<PAD>",
        "<UNK>",
        "<START>",
        "<END>"
    ]

    def __init__(self, vocab_path="brain/vocab.json"):
        self.vocab_path = Path(vocab_path)

        self.vocab = {
            token: index
            for index, token in enumerate(self.SPECIAL_TOKENS)
        }

        self.reverse_vocab = {
            index: token
            for token, index in self.vocab.items()
        }

        if self.vocab_path.exists():
            self.load()

    def tokenize(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        text = text.lower().strip()

        return re.findall(
            r"<[^>\s]+>|[^\W_]+(?:['’][^\W_]+)?|[^\w\s]",
            text,
            flags=re.UNICODE
        )

    def learn(self, text):
        tokens = self.tokenize(text)

        for token in tokens:
            if token not in self.vocab:
                token_id = max(self.reverse_vocab.keys()) + 1

                self.vocab[token] = token_id
                self.reverse_vocab[token_id] = token

        return self.encode(text)

    def learn_batch(self, texts):
        return [
            self.learn(text)
            for text in texts
        ]

    def encode(self, text, add_special_tokens=False):
        token_ids = [
            self.vocab.get(token, self.vocab["<UNK>"])
            for token in self.tokenize(text)
        ]

        if add_special_tokens:
            token_ids = (
                [self.vocab["<START>"]]
                + token_ids
                + [self.vocab["<END>"]]
            )

        return token_ids

    def decode(self, token_ids, skip_special_tokens=True):
        tokens = []

        for token_id in token_ids:
            try:
                token_id = int(token_id)
            except (TypeError, ValueError):
                token = "<UNK>"
            else:
                token = self.reverse_vocab.get(
                    token_id,
                    "<UNK>"
                )

            if skip_special_tokens and token in self.SPECIAL_TOKENS:
                continue

            tokens.append(token)

        result = ""

        closing_punctuation = {
            ".", ",", "!", "?", ";", ":", "%",
            ")", "]", "}", "…"
        }

        opening_punctuation = {"(", "[", "{"}

        for token in tokens:
            if not result:
                result = token

            elif token in closing_punctuation:
                result += token

            elif result[-1:] in opening_punctuation:
                result += token

            else:
                result += " " + token

        return result

    def batch_encode(self, texts):
        return [
            self.encode(text)
            for text in texts
        ]

    def save(self, path=None):
        target = Path(path) if path else self.vocab_path

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = {
            "version": 1,
            "vocab": self.vocab
        }

        temp_path = target.with_suffix(
            target.suffix + ".tmp"
        )

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

        temp_path.replace(target)

    def load(self, path=None):
        target = Path(path) if path else self.vocab_path

        with open(target, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid vocabulary format.")

        vocab = data.get("vocab", data)

        if not isinstance(vocab, dict):
            raise ValueError("Invalid vocabulary format.")

        loaded_vocab = {}

        for token, token_id in vocab.items():
            if not isinstance(token, str):
                raise ValueError("Invalid token.")

            if isinstance(token_id, bool) or not isinstance(
                token_id, int
            ):
                raise ValueError("Token IDs must be integers.")

            if token_id < 0:
                raise ValueError("Token IDs cannot be negative.")

            loaded_vocab[token] = token_id

        if len(set(loaded_vocab.values())) != len(loaded_vocab):
            raise ValueError("Duplicate token IDs found.")

        next_id = max(loaded_vocab.values(), default=-1) + 1

        for token in self.SPECIAL_TOKENS:
            if token not in loaded_vocab:
                loaded_vocab[token] = next_id
                next_id += 1

        self.vocab = loaded_vocab

        self.reverse_vocab = {
            token_id: token
            for token, token_id in self.vocab.items()
        }

        self.vocab_path = target

        return True

    def vocabulary_size(self):
        return len(self.vocab)


if __name__ == "__main__":

    brain = BHTokenizer()

    brain.learn("Hello! Vanakkam! BH OMNI CORE.")

    encoded = brain.encode(
        "Hello BH OMNI CORE",
        add_special_tokens=True
    )

    decoded = brain.decode(encoded)

    print("Tokens:", encoded)
    print("Decoded:", decoded)

    brain.save()

    print("Vocabulary size:", brain.vocabulary_size())
    print("BH-OMNI CORE Tokenizer ready!")
