
import math
from numbers import Real
from pathlib import Path

from brain.neural_network import BHNeuralNetwork


def _validate_training_parameters(epochs, learning_rate):
    if (
        isinstance(epochs, bool)
        or not isinstance(epochs, int)
        or epochs <= 0
    ):
        raise ValueError("Epochs must be a positive integer.")

    if (
        isinstance(learning_rate, bool)
        or not isinstance(learning_rate, Real)
        or not math.isfinite(learning_rate)
        or learning_rate <= 0
    ):
        raise ValueError(
            "Learning rate must be a positive finite number."
        )


def _validate_prediction(prediction):
    if not isinstance(prediction, (list, tuple)):
        raise ValueError(
            "Neural network returned an invalid prediction."
        )

    if len(prediction) != 1:
        raise ValueError(
            "XOR network must return exactly one output."
        )

    value = prediction[0]

    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not math.isfinite(value)
    ):
        raise ValueError(
            "Neural network returned an invalid numeric output."
        )

    return float(value)


def train_xor(epochs=5000, learning_rate=0.5):
    _validate_training_parameters(epochs, learning_rate)

    brain = BHNeuralNetwork(
        input_size=2,
        hidden_size=4,
        output_size=1,
        seed=42
    )

    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
    ]

    print("BH-OMNI CORE: XOR training started")

    for epoch in range(epochs):
        total_loss = 0.0

        for inputs, targets in training_data:
            loss = brain.train(
                inputs,
                targets,
                learning_rate
            )

            if (
                isinstance(loss, bool)
                or not isinstance(loss, Real)
                or not math.isfinite(loss)
            ):
                raise ValueError(
                    "Training produced an invalid loss value."
                )

            total_loss += float(loss)

        if (epoch + 1) % 500 == 0:
            average_loss = total_loss / len(training_data)

            print(
                f"Epoch {epoch + 1}/{epochs} "
                f"| Loss: {average_loss:.6f}"
            )

    output_path = Path(__file__).parent / "xor_weights.json"

    brain.save(output_path)

    print("\nTraining completed!")
    print("Final predictions:")

    passed = 0

    for inputs, targets in training_data:
        prediction = brain.forward(inputs)
        predicted_value = _validate_prediction(prediction)

        correct = (
            predicted_value >= 0.5
        ) == bool(targets[0])

        if correct:
            passed += 1

        print(
            f"Input: {inputs} "
            f"| Expected: {targets[0]} "
            f"| Predicted: {predicted_value:.4f} "
            f"| {'PASS' if correct else 'FAIL'}"
        )

    print(
        f"\nXOR Accuracy: {passed}/{len(training_data)}"
    )

    return brain


if __name__ == "__main__":
    train_xor()
