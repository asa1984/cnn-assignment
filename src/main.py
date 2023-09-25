import argparse
import shutil
from pathlib import Path

import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torchvision

from .train import train
from .validate import validate


def main():
    parser = argparse.ArgumentParser(description="モデルの学習")
    parser.add_argument("--batch", type=int, default=32)
    parser.add_argument("--rate", type=float, default=0.001)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--outDir", type=str, default="models")
    parser.add_argument("--trainData", type=str, default="./dataset/train")
    parser.add_argument("--validateData", type=str, default="./dataset/validate")
    parser.add_argument("--model", type=str, default="model.pth")
    parser.add_argument("--onlyTrain", default=False, action="store_true")
    parser.add_argument("--onlyValidate", default=False, action="store_true")
    opt = parser.parse_args()

    print(opt)

    train_data_dir: str = opt.trainData
    validate_data_dir: str = opt.validateData
    batch_size: int = opt.batch
    learning_rate: float = opt.rate
    epochs: int = opt.epochs
    model_output_dir: str = opt.outDir

    # --onlyValidateオプションの場合、モデルの評価のみ行う
    if opt.onlyValidate:
        validate_transform = transforms.Compose(
            [
                transforms.Resize((64, 64)),
                transforms.ToTensor(),
            ]
        )
        validate_dataset = torchvision.datasets.ImageFolder(
            validate_data_dir, transform=validate_transform
        )
        validate_loader = DataLoader(
            validate_dataset, batch_size=batch_size, shuffle=False
        )
        model_path = f"{model_output_dir}/{opt.model}"
        print("\n===> モデルの評価開始...")
        validate(
            validate_dataset,
            validate_loader,
            model_path,
        )
        print("===> モデルの評価終了")
        return

    print("===> モデルの出力先を新規作成中...")
    try:
        shutil.rmtree(model_output_dir)
    except FileNotFoundError:
        pass
    Path(model_output_dir).mkdir(parents=True, exist_ok=True)

    print("===> データセットを読み込み中...")
    train_transform = transforms.Compose(
        [
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
        ]
    )
    validate_transform = transforms.Compose(
        [
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
        ]
    )
    train_dataset = torchvision.datasets.ImageFolder(
        train_data_dir, transform=train_transform
    )
    validate_dataset = torchvision.datasets.ImageFolder(
        validate_data_dir, transform=validate_transform
    )
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    validate_loader = DataLoader(validate_dataset, batch_size=batch_size, shuffle=False)

    print("\n===> 学習開始...")
    train(
        train_dataset,
        train_loader,
        epochs,
        learning_rate,
        model_output_dir,
    )
    print("===> 学習終了")

    # --onlyTrainオプションの場合はここで終了
    if opt.onlyTrain:
        return

    model_path = f"{model_output_dir}/model.pth"
    print("\n===> モデルの評価開始...")
    validate(
        validate_dataset,
        validate_loader,
        model_path,
    )
    print("===> モデルの評価終了")


main()
