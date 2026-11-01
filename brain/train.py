
from pathlib import Path
from neural_network import BHNeuralNetwork


def train_xor(epochs=5000, learning_rate=0.5):
    brain = BHNeuralNetwork(
        input_size=2,
        hidden_size=4,
        output_size=1
    )

    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
    ]

    for epoch in range(epochs):
        total_loss = 0.0

        for inputs, targets in training_data:
            loss = brain.train(
                inputs,
                targets,
                learning_rate
            )
            total_loss += loss

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

    for inputs, targets in training_data:
        prediction = brain.forward(inputs)

        print(
            f"Input: {inputs} "
            f"| Expected: {targets} "
            f"| Predicted: {prediction}"
        )

    return brain


if __name__ == "__main__":
    train_xor()
