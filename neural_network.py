
import json
import math
import random
from pathlib import Path


class BHNeuralNetwork:

    def __init__(
        self,
        input_size,
        hidden_size,
        output_size,
        seed=None
    ):
        if min(input_size, hidden_size, output_size) <= 0:
            raise ValueError("Network sizes must be positive.")

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.rng = random.Random(seed)

        # Xavier-style initialization
        self.weights = [
            [
                self.rng.uniform(
                    -math.sqrt(6 / (input_size + hidden_size)),
                    math.sqrt(6 / (input_size + hidden_size))
                )
                for _ in range(hidden_size)
            ]
            for _ in range(input_size)
        ]

        self.output_weights = [
            [
                self.rng.uniform(
                    -math.sqrt(6 / (hidden_size + output_size)),
                    math.sqrt(6 / (hidden_size + output_size))
                )
                for _ in range(output_size)
            ]
            for _ in range(hidden_size)
        ]

        self.bias = [0.0] * hidden_size
        self.output_bias = [0.0] * output_size

        self.training_steps = 0
        self.last_loss = None

    def sigmoid(self, x):
        x = max(-60.0, min(60.0, x))
        return 1.0 / (1.0 + math.exp(-x))

    def _validate(self, inputs, targets=None):

        if len(inputs) != self.input_size:
            raise ValueError("Incorrect input size.")

        if not all(math.isfinite(float(x)) for x in inputs):
            raise ValueError("Inputs must be finite numbers.")

        if targets is not None:
            if len(targets) != self.output_size:
                raise ValueError("Incorrect target size.")

            if not all(
                math.isfinite(float(x)) and 0 <= float(x) <= 1
                for x in targets
            ):
                raise ValueError("Targets must be between 0 and 1.")

    def _forward_details(self, inputs):

        self._validate(inputs)

        hidden = []

        for j in range(self.hidden_size):
            total = self.bias[j]

            for i in range(self.input_size):
                total += float(inputs[i]) * self.weights[i][j]

            hidden.append(self.sigmoid(total))

        outputs = []

        for k in range(self.output_size):
            total = self.output_bias[k]

            for j in range(self.hidden_size):
                total += hidden[j] * self.output_weights[j][k]

            outputs.append(self.sigmoid(total))

        return hidden, outputs

    def forward(self, inputs):
        _, outputs = self._forward_details(inputs)
        return outputs

    def train(self, inputs, targets, learning_rate=0.5):

        self._validate(inputs, targets)

        if not math.isfinite(learning_rate) or learning_rate <= 0:
            raise ValueError("Learning rate must be positive.")

        hidden, outputs = self._forward_details(inputs)

        output_deltas = []

        for k in range(self.output_size):
            error = float(targets[k]) - outputs[k]

            output_deltas.append(
                error * outputs[k] * (1 - outputs[k])
            )

        hidden_deltas = []

        for j in range(self.hidden_size):
            error = sum(
                output_deltas[k] * self.output_weights[j][k]
                for k in range(self.output_size)
            )

            hidden_deltas.append(
                error * hidden[j] * (1 - hidden[j])
            )

        # Update output layer
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.output_weights[j][k] += (
                    learning_rate * output_deltas[k] * hidden[j]
                )

        for k in range(self.output_size):
            self.output_bias[k] += learning_rate * output_deltas[k]

        # Update hidden layer
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.weights[i][j] += (
                    learning_rate * hidden_deltas[j] * float(inputs[i])
                )

        for j in range(self.hidden_size):
            self.bias[j] += learning_rate * hidden_deltas[j]

        loss = sum(
            (float(targets[k]) - outputs[k]) ** 2
            for k in range(self.output_size)
        ) / self.output_size

        self.training_steps += 1
        self.last_loss = loss

        return loss

    def train_batch(self, samples, learning_rate=0.5):

        if not samples:
            raise ValueError("Training batch cannot be empty.")

        total_loss = 0.0

        for inputs, targets in samples:
            total_loss += self.train(
                inputs,
                targets,
                learning_rate
            )

        return total_loss / len(samples)

    def evaluate(self, samples):

        if not samples:
            raise ValueError("Evaluation data cannot be empty.")

        total_loss = 0.0

        for inputs, targets in samples:
            self._validate(inputs, targets)

            outputs = self.forward(inputs)

            total_loss += sum(
                (float(targets[k]) - outputs[k]) ** 2
                for k in range(self.output_size)
            ) / self.output_size

        return total_loss / len(samples)

    def save(self, path="brain/weights.json"):

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 2,
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "weights": self.weights,
            "output_weights": self.output_weights,
            "bias": self.bias,
            "output_bias": self.output_bias,
            "training_steps": self.training_steps,
            "last_loss": self.last_loss
        }

        temp_path = path.with_suffix(path.suffix + ".tmp")

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        temp_path.replace(path)

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

        network.training_steps = data.get("training_steps", 0)
        network.last_loss = data.get("last_loss")

        # Validate saved dimensions
        if (
            len(network.weights) != network.input_size
            or any(len(row) != network.hidden_size for row in network.weights)
            or len(network.output_weights) != network.hidden_size
            or any(len(row) != network.output_size for row in network.output_weights)
            or len(network.bias) != network.hidden_size
            or len(network.output_bias) != network.output_size
        ):
            raise ValueError("Saved network dimensions are invalid.")

        return network


if __name__ == "__main__":

    brain = BHNeuralNetwork(2, 4, 1, seed=42)

    samples = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
    ]

    for epoch in range(5000):
        brain.train_batch(samples, learning_rate=0.5)

    print("Training loss:", brain.evaluate(samples))

    for inputs, targets in samples:
        print(inputs, "=>", brain.forward(inputs))

    brain.save()

    print("Training steps:", brain.training_steps)
    print("XOR training demo completed.")
