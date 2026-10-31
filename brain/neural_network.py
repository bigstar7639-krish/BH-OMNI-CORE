
import json
import random
from pathlib import Path


class BHNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.weights = [
            [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
            for _ in range(input_size)
        ]

        self.output_weights = [
            [random.uniform(-0.5, 0.5) for _ in range(output_size)]
            for _ in range(hidden_size)
        ]

        self.bias = [0.0] * hidden_size
        self.output_bias = [0.0] * output_size

    def sigmoid(self, x):
        x = max(-60, min(60, x))
        return 1 / (1 + pow(2.718281828, -x))

    def forward(self, inputs):
        hidden = []

        for j in range(self.hidden_size):
            total = self.bias[j]

            for i in range(self.input_size):
                total += inputs[i] * self.weights[i][j]

            hidden.append(self.sigmoid(total))

        outputs = []

        for k in range(self.output_size):
            total = self.output_bias[k]

            for j in range(self.hidden_size):
                total += hidden[j] * self.output_weights[j][k]

            outputs.append(self.sigmoid(total))

        return outputs

    def save(self, path="brain/weights.json"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        data = {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "weights": self.weights,
            "output_weights": self.output_weights,
            "bias": self.bias,
            "output_bias": self.output_bias
        }

        with open(path, "w") as file:
            json.dump(data, file)

    @classmethod
    def load(cls, path="brain/weights.json"):
        with open(path, "r") as file:
            data = json.load(file)

        network = cls(
            data["input_size"],
            data["hidden_size"],
            data["output_size"]
        )

        network.weights = data["weights"]
        network.output_weights = data["output_weights"]
        network.bias = data["bias"]
        network.output_bias = data["output_bias"]

        return network


if __name__ == "__main__":
    brain = BHNeuralNetwork(4, 8, 2)

    result = brain.forward([1.0, 0.5, 0.2, 0.8])

    print("BH Neural Network:", result)

    brain.save()

    print("Neural network created!")
