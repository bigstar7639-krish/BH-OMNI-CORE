
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
        for name, value in (
            ("input_size", input_size),
            ("hidden_size", hidden_size),
            ("output_size", output_size)
        ):
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value <= 0
            ):
                raise ValueError(f"{name} must be a positive integer.")

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.rng = random.Random(seed)

        limit1 = math.sqrt(6.0 / (input_size + hidden_size))
        limit2 = math.sqrt(6.0 / (hidden_size + output_size))

        self.weights = [
            [
                self.rng.uniform(-limit1, limit1)
                for _ in range(hidden_size)
            ]
            for _ in range(input_size)
        ]

        self.output_weights = [
            [
                self.rng.uniform(-limit2, limit2)
                for _ in range(output_size)
            ]
            for _ in range(hidden_size)
        ]

        self.bias = [0.0] * hidden_size
        self.output_bias = [0.0] * output_size

        self.training_steps = 0
        self.last_loss = None

    @staticmethod
    def _number(value, name):
        if isinstance(value, bool):
            raise TypeError(f"{name} must be a number.")

        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as error:
            raise TypeError(f"{name} must be a number.") from error

        if not math.isfinite(number):
            raise ValueError(f"{name} must be finite.")

        return number

    def sigmoid(self, x):
        x = self._number(x, "Sigmoid input")
        x = max(-60.0, min(60.0, x))
        return 1.0 / (1.0 + math.exp(-x))

    def _validate(self, inputs, targets=None):

        if not isinstance(inputs, (list, tuple)):
            raise TypeError("Inputs must be a list or tuple.")

        if len(inputs) != self.input_size:
            raise ValueError("Incorrect input size.")

        for value in inputs:
            self._number(value, "Input")

        if targets is not None:
            if not isinstance(targets, (list, tuple)):
                raise TypeError("Targets must be a list or tuple.")

            if len(targets) != self.output_size:
                raise ValueError("Incorrect target size.")

            for value in targets:
                number = self._number(value, "Target")

                if not 0.0 <= number <= 1.0:
                    raise ValueError("Targets must be between 0 and 1.")

    def _forward_details(self, inputs):

        self._validate(inputs)

        inputs = [float(value) for value in inputs]

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

        return hidden, outputs

    def forward(self, inputs):
        _, outputs = self._forward_details(inputs)
        return outputs

    def train(self, inputs, targets, learning_rate=0.5):

        self._validate(inputs, targets)

        learning_rate = self._number(
            learning_rate, "Learning rate"
        )

        if learning_rate <= 0:
            raise ValueError("Learning rate must be positive.")

        inputs = [float(value) for value in inputs]
        targets = [float(value) for value in targets]

        hidden, outputs = self._forward_details(inputs)

        output_deltas = []

        for k in range(self.output_size):
            error = targets[k] - outputs[k]

            output_deltas.append(
                error * outputs[k] * (1.0 - outputs[k])
            )

        hidden_deltas = []

        for j in range(self.hidden_size):
            error = sum(
                output_deltas[k] * self.output_weights[j][k]
                for k in range(self.output_size)
            )

            hidden_deltas.append(
                error * hidden[j] * (1.0 - hidden[j])
            )

        # Update output layer
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.output_weights[j][k] += (
                    learning_rate * output_deltas[k] * hidden[j]
                )

        for k in range(self.output_size):
            self.output_bias[k] += (
                learning_rate * output_deltas[k]
            )

        # Update hidden layer
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.weights[i][j] += (
                    learning_rate * hidden_deltas[j] * inputs[i]
                )

        for j in range(self.hidden_size):
            self.bias[j] += learning_rate * hidden_deltas[j]

        loss = sum(
            (targets[k] - outputs[k]) ** 2
            for k in range(self.output_size)
        ) / self.output_size

        self.training_steps += 1
        self.last_loss = loss

        return loss

    def train_batch(self, samples, learning_rate=0.5):

        if not isinstance(samples, (list, tuple)) or not samples:
            raise ValueError("Training batch cannot be empty.")

        learning_rate = self._number(
            learning_rate, "Learning rate"
        )

        if learning_rate <= 0:
            raise ValueError("Learning rate must be positive.")

        # Validate the entire batch before changing network weights.
        validated_samples = []

        for sample in samples:
            if not isinstance(sample, (list, tuple)) or len(sample) != 2:
                raise ValueError(
                    "Each training sample must contain inputs and targets."
                )

            inputs, targets = sample
            self._validate(inputs, targets)

            validated_samples.append((
                list(inputs),
                list(targets)
            ))

        total_loss = 0.0

        for inputs, targets in validated_samples:
            total_loss += self.train(
                inputs,
                targets,
                learning_rate
            )

        return total_loss / len(validated_samples)

    def evaluate(self, samples):

        if not isinstance(samples, (list, tuple)) or not samples:
            raise ValueError("Evaluation data cannot be empty.")

        validated_samples = []

        for sample in samples:
            if not isinstance(sample, (list, tuple)) or len(sample) != 2:
                raise ValueError(
                    "Each evaluation sample must contain inputs and targets."
                )

            inputs, targets = sample
            self._validate(inputs, targets)

            validated_samples.append((
                list(inputs),
                list(targets)
            ))

        total_loss = 0.0

        for inputs, targets in validated_samples:
            outputs = self.forward(inputs)

            total_loss += sum(
                (float(targets[k]) - outputs[k]) ** 2
                for k in range(self.output_size)
            ) / self.output_size

        return total_loss / len(validated_samples)

    def _validate_parameters(self):

        expected_shapes = (
            (self.weights, self.input_size, self.hidden_size, "weights"),
            (
                self.output_weights,
                self.hidden_size,
                self.output_size,
                "output_weights"
            )
        )

        for matrix, rows, columns, name in expected_shapes:
            if not isinstance(matrix, list) or len(matrix) != rows:
                raise ValueError(f"Invalid {name} dimensions.")

            for row in matrix:
                if not isinstance(row, list) or len(row) != columns:
                    raise ValueError(f"Invalid {name} dimensions.")

                for value in row:
                    self._number(value, name)

        for values, expected, name in (
            (self.bias, self.hidden_size, "bias"),
            (self.output_bias, self.output_size, "output_bias")
        ):
            if not isinstance(values, list) or len(values) != expected:
                raise ValueError(f"Invalid {name} dimensions.")

            for value in values:
                self._number(value, name)

        if (
            not isinstance(self.training_steps, int)
            or isinstance(self.training_steps, bool)
            or self.training_steps < 0
        ):
            raise ValueError("Invalid training_steps.")

        if self.last_loss is not None:
            loss = self._number(self.last_loss, "last_loss")

            if loss < 0:
                raise ValueError("last_loss cannot be negative.")

    def save(self, path="brain/weights.json"):

        self._validate_parameters()

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

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False
                )
                file.flush()

            temp_path.replace(path)

        except OSError:
            try:
                if temp_path.exists():
                    temp_path.unlink()
            except OSError:
                pass

            raise

        return True

    @classmethod
    def load(cls, path="brain/weights.json"):

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError("Saved network file contains invalid JSON.") from error

        if not isinstance(data, dict):
            raise ValueError("Saved network data must be a JSON object.")

        required = (
            "input_size",
            "hidden_size",
            "output_size",
            "weights",
            "output_weights",
            "bias",
            "output_bias"
        )

        for key in required:
            if key not in data:
                raise ValueError(f"Missing saved network field: {key}")

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

        network._validate_parameters()

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

    loaded_brain = BHNeuralNetwork.load()

    print("Loaded network:", loaded_brain.forward([0, 1]))
    print("Training steps:", brain.training_steps)
    print("XOR training demo completed.")
