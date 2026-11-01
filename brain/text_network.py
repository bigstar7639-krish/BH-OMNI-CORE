
from brain.neural_network import BHNeuralNetwork
from brain.text_feature_engine import BHTextFeatureEngine


class BHTextNetwork:

    INPUT_SIZE = 4
    DEFAULT_HIDDEN_SIZE = 8
    DEFAULT_OUTPUT_SIZE = 2
    DEFAULT_PATH = "brain/text_network_weights.json"

    def __init__(
        self,
        hidden_size=DEFAULT_HIDDEN_SIZE,
        output_size=DEFAULT_OUTPUT_SIZE,
        seed=42
    ):
        self.feature_engine = BHTextFeatureEngine()

        self.network = BHNeuralNetwork(
            input_size=self.INPUT_SIZE,
            hidden_size=hidden_size,
            output_size=output_size,
            seed=seed
        )

    @staticmethod
    def _validate_text(text):
        if not isinstance(text, str):
            raise TypeError("Text input must be a string.")

        if not text.strip():
            raise ValueError("Text input cannot be empty.")

    def _extract_features(self, text):
        self._validate_text(text)

        features = self.feature_engine.text_to_features(text)

        if not isinstance(features, (list, tuple)):
            raise TypeError(
                "Text feature engine must return a list or tuple."
            )

        if len(features) != self.INPUT_SIZE:
            raise ValueError(
                f"Expected {self.INPUT_SIZE} text features, "
                f"received {len(features)}."
            )

        return features

    # Process text
    def forward_text(self, text):
        features = self._extract_features(text)
        output = self.network.forward(features)

        return {
            "features": features,
            "output": output
        }

    # Train using text
    def train_text(
        self,
        text,
        targets,
        learning_rate=0.5
    ):
        features = self._extract_features(text)

        return self.network.train(
            features,
            targets,
            learning_rate
        )

    # Save network weights
    def save(self, path=DEFAULT_PATH):
        return self.network.save(path)

    # Load saved network weights
    @classmethod
    def load(cls, path=DEFAULT_PATH):
        instance = cls.__new__(cls)

        instance.feature_engine = BHTextFeatureEngine()
        instance.network = BHNeuralNetwork.load(path)

        if instance.network.input_size != cls.INPUT_SIZE:
            raise ValueError(
                "Loaded text network must have exactly "
                f"{cls.INPUT_SIZE} input features."
            )

        if not callable(
            getattr(instance.network, "forward", None)
        ):
            raise TypeError(
                "Loaded network does not have a valid forward method."
            )

        if not callable(
            getattr(instance.network, "train", None)
        ):
            raise TypeError(
                "Loaded network does not have a valid train method."
            )

        return instance


if __name__ == "__main__":

    text_brain = BHTextNetwork()

    result = text_brain.forward_text("What is Earth?")

    print("Features:", result["features"])
    print("Output:", result["output"])
