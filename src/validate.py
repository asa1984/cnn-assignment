import torch

from .model import CustomNet


def validate(
    validate_dataset,
    validate_loader,
    model_path,
):
    classes = validate_dataset.classes
    count_classes = len(classes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CustomNet(count_classes).to(device)
    model.load_state_dict(torch.load(model_path))

    correct_predictions = {classname: 0 for classname in classes}
    total_predictions = {classname: 0 for classname in classes}

    with torch.no_grad():
        for inputs, labels in validate_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)

            _, predictions = torch.max(outputs.data, 1)

            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct_predictions[classes[label]] += 1
                total_predictions[classes[label]] += 1

    print("====> クラス別正解率")

    for classname, correct_count in correct_predictions.items():
        accuracy = 100 * correct_count / total_predictions[classname]

        print(
            f"{classname}: {accuracy:.2f}% ({correct_count}/{total_predictions[classname]})"
        )

    print("====> 総合正解率")
    total_accuracy = (
        100 * sum(correct_predictions.values()) / sum(total_predictions.values())
    )
    print(f"{total_accuracy:.2f}%")
