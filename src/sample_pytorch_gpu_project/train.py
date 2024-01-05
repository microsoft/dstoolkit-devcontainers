import argparse
from pathlib import Path

import mlflow
import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa: N812
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms


# Example model, delete or replace with your own
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def main(args):
    # keep this setup code
    print("\n".join(f"{k}: {v}" for k, v in sorted(dict(vars(args)).items())))
    dict_args = vars(args)
    args.train_artifacts_dir.mkdir(parents=True, exist_ok=True)
    mlflow.autolog()
    mlflow.log_params(dict_args)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

    # code below this comment is a sample only, replace with your own training code

    # transforms.Normalize() uses Imagenet means and stds
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    trainset = torchvision.datasets.CIFAR10(
        root="./data", train=True, download=True, transform=transform
    )
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=args.batch_size, shuffle=True, num_workers=2
    )

    net = Net()
    net.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(2):  # loop over the dataset multiple times
        mini_batch_loss = 0.0
        for i, data in enumerate(trainloader):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data[0].to(device), data[1].to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            mini_batch_loss += loss.item()
            if (i + 1) % 2000 == 0:  # print every 2000 mini-batches
                print(f"[{epoch + 1}, {i + 1:5d}] loss: {mini_batch_loss / 2000:.3f}")
                mlflow.log_metric(
                    "Training Loss",
                    mini_batch_loss / 2000,
                    step=i + (epoch * len(trainloader)),
                )
                mini_batch_loss = 0.0

    print("Finished Training")

    # save model
    torch.save(net.state_dict(), args.train_artifacts_dir / "cifar_net.pth")
    print(f"Model saved to {args.train_artifacts_dir / 'cifar_net.pth'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_artifacts_dir",
        type=Path,
        help="output directory where trained model, checkpoints etc are saved",
        default=Path("outputs"),
    )
    parser.add_argument(
        "--batch_size", type=int, help="the training batch size", default=4
    )
    args = parser.parse_args()
    main(args)
