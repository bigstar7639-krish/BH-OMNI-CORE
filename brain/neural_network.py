
import json
import math
import random
from pathlib import Path


class BHNeuralNetwork:

    def __init__(self, input_size, hidden_size, output_size):
        if min(input_size, hidden_size, output_size) <= 0:
            raise ValueError("Network sizes must be positive.")

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
        x = max(-60.0, min(60.0, x))
        return 1.0 / (1.0 + math.exp(-x))

    def forward(self, inputs):
        if len(inputs) != self.input_size:
            raise ValueError("Incorrect input size.")

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

    def train(self, inputs, targets, learning_rate=0.5):
        if len(inputs) != self.input_size:
            raise ValueError("Incorrect input size.")

        if len(targets) != self.output_size:
            raise ValueError("Incorrect target size.")

        if learning_rate <= 0:
            raise ValueError("Learning rate must be positive.")

        # Forward pass
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

        # Output error gradients
        output_deltas = []

        for k in range(self.output_size):
            error = targets[k] - outputs[k]
            delta = error * outputs[k] * (1 - outputs[k])
            output_deltas.append(delta)

        # Hidden layer gradients
        hidden_deltas = []

        for j in range(self.hidden_size):
            error = 0.0

            for k in range(self.output_size):
                error += output_deltas[k] * self.output_weights[j][k]

            delta = error * hidden[j] * (1 - hidden[j])
            hidden_deltas.append(delta)

        # Update output weights
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.output_weights[j][k] += (
                    learning_rate * output_deltas[k] * hidden[j]
                )

        for k in range(self.output_size):
            self.output_bias[k] += learning_rate * output_deltas[k]

        # Update hidden weights
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.weights[i][j] += (
                    learning_rate * hidden_deltas[j] * inputs[i]
                )

        for j in range(self.hidden_size):
            self.bias[j] += learning_rate * hidden_deltas[j]

        return sum(
            (targets[k] - outputs[k]) ** 2
            for k in range(self.output_size)
        ) / self.output_size

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

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load(cls, path="brain/weights.json"):
        with open(path, "r", encoding="utf-8") as file:
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
    brain = BHNeuralNetwork(2, 4, 1)

    for epoch in range(5000):
        brain.train([0, 0], [0])
        brain.train([0, 1], [1])
        brain.train([1, 0], [1])
        brain.train([1, 1], [0])

    for inputs in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(inputs, "=>", brain.forward(inputs))

    brain.save()
    print("XOR training demo completed.")
