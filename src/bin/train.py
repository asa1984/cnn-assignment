import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torchvision

from ..model import CustomNet


TRAIN_DATA_DIR = "./dataset/train"


# パラメータ
batch_size = 64
learning_rate = 0.001
num_epochs = 10


# データの前処理
transform = transforms.Compose(
    [
        transforms.Resize((140, 140)),
        transforms.ToTensor(),
    ]
)

# データセットの読み込み
train_dataset = torchvision.datasets.ImageFolder(TRAIN_DATA_DIR, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# モデルの構築
num_classes = len(train_dataset.classes)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CustomNet(num_classes).to(device)

# 損失関数とオプティマイザ
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)


# 学習ループ
print("Start Training")

for epoch in range(num_epochs):
    running_loss = 0.0
    for inputs, labels in train_loader:
        # inputs = torch.stack(inputs).to(device)
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(train_loader)}")

print("Finished Training")


# モデルの保存
SAVE_PATH = "./model.pth"
torch.save(model.state_dict(), SAVE_PATH)
print(f"Saved pytorch model state to {SAVE_PATH}")
