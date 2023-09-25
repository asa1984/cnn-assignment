import torch.nn as nn


class CustomNet(nn.Module):
    def __init__(self, num_classes):
        super(CustomNet, self).__init__()
        # 畳み込み層1
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()

        # プーリング層1
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 畳み込み層2
        self.conv2 = nn.Conv2d(
            in_channels=16, out_channels=32, kernel_size=3, padding=1
        )
        self.relu2 = nn.ReLU()

        # プーリング層2
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 全結合層1
        self.fc1 = nn.Linear(32 * 16 * 16, 128)
        self.relu3 = nn.ReLU()

        # 全結合層2
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return x
