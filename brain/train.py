
from neural_network import BHNeuralNetwork


def train():
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

    learning_rate = 0.5
    epochs = 10000

    for epoch in range(epochs):
        total_error = 0

        for inputs, targets in training_data:

            hidden = []
            for j in range(brain.hidden_size):
                value = brain.bias[j]

                for i in range(brain.input_size):
                    value += inputs[i] * brain.weights[i][j]

                hidden.append(brain.sigmoid(value))

            outputs = brain.forward(inputs)

            output_errors = [
                targets[k] - outputs[k]
                for k in range(brain.output_size)
            ]

            output_deltas = [
                output_errors[k] * outputs[k] * (1 - outputs[k])
                for k in range(brain.output_size)
            ]

            hidden_deltas = []

            for j in range(brain.hidden_size):
                error = sum(
                    output_deltas[k] * brain.output_weights[j][k]
                    for k in range(brain.output_size)
                )

                hidden_deltas.append(
                    error * hidden[j] * (1 - hidden[j])
                )

            for j in range(brain.hidden_size):
                for k in range(brain.output_size):
                    brain.output_weights[j][k] += (
                        learning_rate * hidden[j] * output_deltas[k]
                    )

            for k in range(brain.output_size):
                brain.output_bias[k] += learning_rate * output_deltas[k]

            for i in range(brain.input_size):
                for j in range(brain.hidden_size):
                    brain.weights[i][j] += (
                        learning_rate * inputs[i] * hidden_deltas[j]
                    )

            for j in range(brain.hidden_size):
                brain.bias[j] += learning_rate * hidden_deltas[j]

            total_error += sum(e * e for e in output_errors)

        if epoch % 1000 == 0:
            print("Epoch:", epoch, "Error:", total_error)

    brain.save()
    print("BH-OMNI CORE training completed!")

    for inputs, targets in training_data:
        print(inputs, "=>", brain.forward(inputs))


if __name__ == "__main__":
    train()
