
import re
import json
from pathlib import Path


class BHTokenizer:

    def __init__(self):
        self.vocab = {
            "<PAD>": 0,
            "<UNK>": 1,
            "<START>": 2,
            "<END>": 3
        }

        self.reverse_vocab = {
            value: key for key, value in self.vocab.items()
        }

    def tokenize(self, text):
        return re.findall(r"\w+|[^\w\s]", str(text).lower())

    def learn(self, text):
        for token in self.tokenize(text):
            if token not in self.vocab:
                token_id = len(self.vocab)
                self.vocab[token] = token_id
                self.reverse_vocab[token_id] = token

        return self.encode(text)

    def encode(self, text):
        return [
            self.vocab.get(token, self.vocab["<UNK>"])
            for token in self.tokenize(text)
        ]

    def decode(self, token_ids):
        tokens = [
            self.reverse_vocab.get(int(token_id), "<UNK>")
            for token_id in token_ids
        ]

        return " ".join(tokens)

    def save(self, path="brain/vocab.json"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                self.vocab,
                file,
                ensure_ascii=False,
                indent=2
            )

    def load(self, path="brain/vocab.json"):
        with open(path, "r", encoding="utf-8") as file:
            vocab = json.load(file)

        self.vocab = {
            token: int(token_id)
            for token, token_id in vocab.items()
        }

        self.reverse_vocab = {
            value: key for key, value in self.vocab.items()
        }


if __name__ == "__main__":
    brain = BHTokenizer()

    brain.learn("Hello! Vanakkam! BH OMNI CORE.")

    encoded = brain.encode("Hello BH OMNI CORE")
    decoded = brain.decode(encoded)

    print("Tokens:", encoded)
    print("Decoded:", decoded)

    brain.save()

    print("BH Tokenizer ready!")
