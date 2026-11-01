
from brain.neural_network import BHNeuralNetwork
from brain.text_feature_engine import BHTextFeatureEngine


class BHTextNetwork:

    def __init__(
        self,
        hidden_size=8,
        output_size=2,
        seed=42
    ):
        self.feature_engine = BHTextFeatureEngine()

        self.network = BHNeuralNetwork(
            input_size=4,
            hidden_size=hidden_size,
            output_size=output_size,
            seed=seed
        )

    # Convert text and get network output
    def forward_text(self, text):

        features = self.feature_engine.text_to_features(text)

        output = self.network.forward(features)

        return {
            "features": features,
            "output": output
        }

    # Train using text and target values
    def train_text(
        self,
        text,
        targets,
        learning_rate=0.5
    ):
        features = self.feature_engine.text_to_features(text)

        return self.network.train(
            features,
            targets,
            learning_rate
        )

    # Save trained network
    def save(self, path="brain/text_network_weights.json"):
        self.network.save(path)

    # Load trained network
    @classmethod
    def load(cls, path="brain/text_network_weights.json"):

        instance = cls.__new__(cls)

        instance.feature_engine = BHTextFeatureEngine()
        instance.network = BHNeuralNetwork.load(path)

        if instance.network.input_size != 4:
            raise ValueError("Text network requires 4 input features.")

        return instance


if __name__ == "__main__":

    text_brain = BHTextNetwork()

    result = text_brain.forward_text(
        "What is Earth?"
    )

    print("Text features:", result["features"])
    print("Network output:", result["output"])
