import torch
import torch.nn as nn
import torch.optim as optim

import matplotlib.pyplot as plt

from .model import CustomNet


def train(
    train_dataset,
    train_loader,
    epochs: int,
    learning_rate: float,
    model_output_dir: str,
):
    count_classes = len(train_dataset.classes)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CustomNet(count_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Matplotlib: 損失を記録
    loss_history = []

    def train_one_epoch(epoch: int):
        total_loss = 0.0
        total_batches = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_batches += 1

        average_loss = total_loss / total_batches
        print(f"====> エポック {epoch}/{epochs}, 平均損失: {average_loss}")

        # Matplotlib: 損失を記録
        loss_history.append(average_loss)

    def save_model(epoch: int):
        model_output_path = f"./{model_output_dir}/model_epoch_{epoch}.pth"
        torch.save(model.state_dict(), model_output_path)
        print(f"モデルを{model_output_path}に保存")

    for epoch in range(1, epochs + 1):
        train_one_epoch(epoch)
        save_model(epoch)

    print("====> モデルを保存中...")
    save_path = f"./{model_output_dir}/model.pth"
    torch.save(model.state_dict(), save_path)
    print(f"モデルを{save_path}に保存")

    # Matplotlib: グラフに描画
    plt.figure()
    plt.figure()
    plt.plot(range(1, epochs + 1), loss_history, marker="o")
    plt.xlabel("epoch")
    plt.ylabel("average loss")
    plt.title("loss history")
    plt.grid(True)
    plt.savefig(f"./loss_plot.png")
    plt.show()
