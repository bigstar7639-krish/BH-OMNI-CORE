
import json
import unicodedata
from pathlib import Path


class BHTokenizer:
    """Unicode-aware tokenizer for multilingual text experiments."""

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

    @staticmethod
    def _is_mark(character):
        return unicodedata.category(character).startswith("M")

    @staticmethod
    def _is_letter(character):
        return unicodedata.category(character).startswith("L")

    @staticmethod
    def _is_number(character):
        return unicodedata.category(character).startswith("N")

    @staticmethod
    def _is_cjk_ideograph(character):
        code = ord(character)

        return (
            0x3400 <= code <= 0x4DBF
            or 0x4E00 <= code <= 0x9FFF
            or 0xF900 <= code <= 0xFAFF
            or 0x20000 <= code <= 0x2FA1F
        )

    @staticmethod
    def _is_joiner(character):
        return character in ("\u200c", "\u200d")

    @staticmethod
    def _is_variation_selector(character):
        code = ord(character)

        return (
            0xFE00 <= code <= 0xFE0F
            or 0xE0100 <= code <= 0xE01EF
        )

    @classmethod
    def _is_word_character(cls, character):
        return (
            cls._is_letter(character)
            or cls._is_mark(character)
            or cls._is_number(character)
        )

    @classmethod
    def _append_word_character(cls, current, character):
        if cls._is_mark(character):
            return bool(current)

        if cls._is_joiner(character):
            return bool(current)

        return cls._is_word_character(character)

    @classmethod
    def tokenize(cls, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        text = unicodedata.normalize("NFC", text).casefold()

        tokens = []
        current = []
        index = 0

        def flush():
            if current:
                tokens.append("".join(current))
                current.clear()

        while index < len(text):
            character = text[index]

            # Preserve known special-token syntax.
            if character == "<":
                end = text.find(">", index + 1)

                if end != -1:
                    candidate = text[index:end + 1]

                    if (
                        candidate in cls.SPECIAL_TOKENS
                        or (
                            candidate.startswith("<")
                            and candidate.endswith(">")
                            and len(candidate) > 2
                            and not any(c.isspace() for c in candidate)
                        )
                    ):
                        flush()
                        tokens.append(candidate)
                        index = end + 1
                        continue

            # Whitespace separates tokens.
            if character.isspace():
                flush()
                index += 1
                continue

            # CJK ideographs are separated individually.
            # This is a basic fallback, not dictionary-based word segmentation.
            if cls._is_cjk_ideograph(character):
                flush()
                tokens.append(character)
                index += 1
                continue

            # Letters, numbers and combining marks.
            if cls._append_word_character(current, character):
                current.append(character)
                index += 1
                continue

            # Apostrophes are retained inside words.
            if character in ("'", "’") and current:
                next_index = index + 1

                if (
                    next_index < len(text)
                    and cls._is_letter(text[next_index])
                ):
                    current.append(character)
                    index += 1
                    continue

            # Keep emoji variation selectors and joined emoji sequences.
            if (
                cls._is_variation_selector(character)
                or cls._is_joiner(character)
            ):
                if current:
                    current.append(character)
                else:
                    flush()
                    tokens.append(character)

                index += 1
                continue

            # Other symbols and punctuation become separate tokens.
            flush()
            tokens.append(character)
            index += 1

        flush()
        return tokens

    def learn(self, text):
        tokens = self.tokenize(text)

        for token in tokens:
            if token not in self.vocab:
                token_id = max(self.reverse_vocab.keys()) + 1

                self.vocab[token] = token_id
                self.reverse_vocab[token_id] = token

        return self.encode(text)

    def learn_batch(self, texts):
        if not isinstance(texts, (list, tuple)):
            raise TypeError("texts must be a list or tuple.")

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
        if not isinstance(token_ids, (list, tuple)):
            raise TypeError("token_ids must be a list or tuple.")

        tokens = []

        for token_id in token_ids:
            try:
                token_id = int(token_id)
            except (TypeError, ValueError, OverflowError):
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
            ")", "]", "}", "…", "。", "、",
            "！", "？", "，", "；", "："
        }

        opening_punctuation = {
            "(", "[", "{", "（", "「", "『"
        }

        no_space_scripts = (
            "CJK UNIFIED IDEOGRAPH",
            "HIRAGANA",
            "KATAKANA",
            "HANGUL",
            "THAI",
            "LAO",
            "KHMER",
            "MYANMAR"
        )

        for token in tokens:
            if not result:
                result = token
                continue

            if token in closing_punctuation:
                result += token
                continue

            if result[-1:] in opening_punctuation:
                result += token
                continue

            previous_name = unicodedata.name(
                result[-1],
                ""
            )

            current_name = unicodedata.name(
                token[0],
                ""
            )

            previous_no_space = any(
                script in previous_name
                for script in no_space_scripts
            )

            current_no_space = any(
                script in current_name
                for script in no_space_scripts
            )

            if previous_no_space or current_no_space:
                result += token
            else:
                result += " " + token

        return result

    def batch_encode(self, texts):
        if not isinstance(texts, (list, tuple)):
            raise TypeError("texts must be a list or tuple.")

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

        try:
            with open(
                temp_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            temp_path.replace(target)

        finally:
            if temp_path.exists():
                temp_path.unlink()

        return True

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
            if not isinstance(token, str) or not token:
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

        # Existing special-token IDs must remain stable.
        for index, token in enumerate(self.SPECIAL_TOKENS):
            if token in loaded_vocab and loaded_vocab[token] != index:
                raise ValueError(
                    f"Invalid ID for special token: {token}"
                )

        next_id = max(loaded_vocab.values(), default=-1) + 1

        for index, token in enumerate(self.SPECIAL_TOKENS):
            if token not in loaded_vocab:
                loaded_vocab[token] = index

        if len(set(loaded_vocab.values())) != len(loaded_vocab):
            raise ValueError("Special token ID conflict.")

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

    samples = [
        "Hello! BH OMNI CORE.",
        "வணக்கம் தமிழ் உலகம்",
        "नमस्ते दुनिया",
        "مرحبا بالعالم",
        "你好世界",
        "こんにちは世界",
        "안녕하세요 세계",
        "Привет мир"
    ]

    for sample in samples:
        brain.learn(sample)
        print("Input:", sample)
        print("Tokens:", brain.tokenize(sample))
        print("Decoded:", brain.decode(brain.encode(sample)))
        print()

    brain.save()

    print("Vocabulary size:", brain.vocabulary_size())
    print("BH-OMNI CORE multilingual tokenizer ready!")
