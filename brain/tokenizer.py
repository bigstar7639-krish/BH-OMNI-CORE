
import json
import unicodedata
from pathlib import Path


class BHTokenizer:
    """Unicode-aware tokenizer for multilingual text experiments."""

    SPECIAL_TOKENS = ["<PAD>", "<UNK>", "<START>", "<END>"]

    NO_SPACE_SCRIPTS = (
        "THAI", "LAO", "KHMER", "MYANMAR",
        "HIRAGANA", "KATAKANA", "HANGUL",
        "CJK UNIFIED IDEOGRAPH"
    )

    def __init__(self, vocab_path="brain/vocab.json"):
        self.vocab_path = Path(vocab_path)
        self.vocab = {
            token: index
            for index, token in enumerate(self.SPECIAL_TOKENS)
        }
        self.reverse_vocab = {
            index: token for token, index in self.vocab.items()
        }

        if self.vocab_path.exists():
            self.load()

    @staticmethod
    def _category(char):
        return unicodedata.category(char)

    @staticmethod
    def _is_mark(char):
        return unicodedata.category(char).startswith("M")

    @staticmethod
    def _is_letter(char):
        return unicodedata.category(char).startswith("L")

    @staticmethod
    def _is_number(char):
        return unicodedata.category(char).startswith("N")

    @staticmethod
    def _is_joiner(char):
        return char in ("\u200c", "\u200d")

    @staticmethod
    def _is_variation_selector(char):
        code = ord(char)
        return (
            0xFE00 <= code <= 0xFE0F
            or 0xE0100 <= code <= 0xE01EF
        )

    @staticmethod
    def _is_cjk_ideograph(char):
        code = ord(char)
        return (
            0x3400 <= code <= 0x4DBF
            or 0x4E00 <= code <= 0x9FFF
            or 0xF900 <= code <= 0xFAFF
            or 0x20000 <= code <= 0x2FA1F
        )

    @classmethod
    def _script_name(cls, char):
        return unicodedata.name(char, "").split(" ")[0]

    @classmethod
    def _is_cluster_script(cls, char):
        name = unicodedata.name(char, "")
        return any(script in name for script in cls.NO_SPACE_SCRIPTS)

    @classmethod
    def tokenize(cls, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        text = unicodedata.normalize("NFC", text).casefold()
        tokens = []
        current = []
        cluster = []

        def flush_word():
            if current:
                tokens.append("".join(current))
                current.clear()

        def flush_cluster():
            if cluster:
                tokens.append("".join(cluster))
                cluster.clear()

        index = 0

        while index < len(text):
            char = text[index]

            if char == "<":
                end = text.find(">", index + 1)
                if end != -1:
                    candidate = text[index:end + 1]
                    if (
                        candidate in cls.SPECIAL_TOKENS
                        or (
                            len(candidate) > 2
                            and not any(c.isspace() for c in candidate)
                        )
                    ):
                        flush_cluster()
                        flush_word()
                        tokens.append(candidate)
                        index = end + 1
                        continue

            if char.isspace():
                flush_cluster()
                flush_word()
                index += 1
                continue

            if cls._is_cjk_ideograph(char):
                flush_cluster()
                flush_word()
                tokens.append(char)
                index += 1
                continue

            if cls._is_cluster_script(char):
                flush_word()

                if cls._is_letter(char):
                    flush_cluster()
                    cluster.append(char)
                elif cls._is_mark(char) or cls._is_joiner(char):
                    if cluster:
                        cluster.append(char)
                    else:
                        tokens.append(char)
                else:
                    flush_cluster()
                    tokens.append(char)

                index += 1
                continue

            if cls._is_mark(char) or cls._is_joiner(char):
                if current:
                    current.append(char)
                elif cluster:
                    cluster.append(char)
                else:
                    tokens.append(char)
                index += 1
                continue

            if cls._is_letter(char) or cls._is_number(char):
                flush_cluster()
                current.append(char)
                index += 1
                continue

            if char in ("'", "’") and current:
                if (
                    index + 1 < len(text)
                    and cls._is_letter(text[index + 1])
                ):
                    current.append(char)
                    index += 1
                    continue

            if cls._is_variation_selector(char):
                if current:
                    current.append(char)
                elif cluster:
                    cluster.append(char)
                else:
                    tokens.append(char)
                index += 1
                continue

            flush_cluster()
            flush_word()
            tokens.append(char)
            index += 1

        flush_cluster()
        flush_word()
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
        return [self.learn(text) for text in texts]

    def encode(self, text, add_special_tokens=False):
        ids = [
            self.vocab.get(token, self.vocab["<UNK>"])
            for token in self.tokenize(text)
        ]

        if add_special_tokens:
            ids = (
                [self.vocab["<START>"]]
                + ids
                + [self.vocab["<END>"]]
            )

        return ids

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
                token = self.reverse_vocab.get(token_id, "<UNK>")

            if skip_special_tokens and token in self.SPECIAL_TOKENS:
                continue

            tokens.append(token)

        result = ""
        closing = {
            ".", ",", "!", "?", ";", ":", "%",
            ")", "]", "}", "…", "。", "、",
            "！", "？", "，", "；", "："
        }
        opening = {"(", "[", "{", "（", "「", "『"}

        for token in tokens:
            if not result:
                result = token
                continue

            if token in closing or result[-1:] in opening:
                result += token
                continue

            previous = unicodedata.name(result[-1], "")
            current = unicodedata.name(token[0], "")

            no_space = any(
                script in previous or script in current
                for script in self.NO_SPACE_SCRIPTS
            )

            result += token if no_space else " " + token

        return result

    def batch_encode(self, texts):
        if not isinstance(texts, (list, tuple)):
            raise TypeError("texts must be a list or tuple.")
        return [self.encode(text) for text in texts]

    def save(self, path=None):
        target = Path(path) if path else self.vocab_path
        target.parent.mkdir(parents=True, exist_ok=True)

        data = {"version": 1, "vocab": self.vocab}
        temp = target.with_suffix(target.suffix + ".tmp")

        try:
            with temp.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.flush()
            temp.replace(target)
        finally:
            if temp.exists():
                temp.unlink()

        return True

    def load(self, path=None):
        target = Path(path) if path else self.vocab_path

        with target.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid vocabulary format.")

        vocab = data.get("vocab", data)
        if not isinstance(vocab, dict):
            raise ValueError("Invalid vocabulary format.")

        loaded = {}

        for token, token_id in vocab.items():
            if not isinstance(token, str) or not token:
                raise ValueError("Invalid token.")
            if isinstance(token_id, bool) or not isinstance(token_id, int):
                raise ValueError("Token IDs must be integers.")
            if token_id < 0:
                raise ValueError("Token IDs cannot be negative.")
            loaded[token] = token_id

        if len(set(loaded.values())) != len(loaded):
            raise ValueError("Duplicate token IDs found.")

        for index, token in enumerate(self.SPECIAL_TOKENS):
            if token in loaded and loaded[token] != index:
                raise ValueError("Invalid special-token ID.")

        for index, token in enumerate(self.SPECIAL_TOKENS):
            loaded.setdefault(token, index)

        if len(set(loaded.values())) != len(loaded):
            raise ValueError("Special token ID conflict.")

        self.vocab = loaded
        self.reverse_vocab = {
            token_id: token for token, token_id in loaded.items()
        }
        self.vocab_path = target
        return True

    def vocabulary_size(self):
        return len(self.vocab)
