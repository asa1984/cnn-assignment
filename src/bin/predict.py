import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torchvision

from ..model import CustomNet


VALIDATION_DATA_DIR = "./dataset/val"


# パラメータ
batch_size = 64


# データの前処理
transform = transforms.Compose(
    [
        transforms.Resize((140, 140)),
        transforms.ToTensor(),
    ]
)

# データセットの読み込み
validation_dataset = torchvision.datasets.ImageFolder(
    VALIDATION_DATA_DIR, transform=transform
)
validation_loader = DataLoader(validation_dataset, batch_size=batch_size)

# モデルの構築
num_classes = len(validation_dataset.classes)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CustomNet(num_classes=num_classes).to(device)
model.load_state_dict(torch.load("./model.pth"))


# 推論
model.eval()

correct = 0
total = 0
predictions = []

with torch.no_grad():
    for inputs, labels in validation_loader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        predictions.extend(predicted.cpu().numpy())

print(f"データ数: {total}")
print(f"正解数: {correct}")
print(f"正解率: {(100 * correct / total):.2f}%")

# 推論結果と正答を列挙
print("誤答:")
class_names = validation_dataset.classes
for i in range(len(predictions)):
    if predictions[i] != validation_dataset[i][1]:
        print(
            f"☓: {class_names[predictions[i]]}, 〇: {class_names[validation_dataset[i][1]]}"
        )
