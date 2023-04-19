import argparse
from pathlib import Path
from train import Net
import mlflow
import torch
import torchvision
import torchvision.transforms as transforms
import pandas as pd


def main(args):
    print(
        "\n".join("%s: %s" % (k, str(v)) for k, v in sorted(dict(vars(args)).items()))
    )
    mlflow.autolog()

    net = Net()
    net.load_state_dict(torch.load(args.train_artifacts_dir / 'cifar_net.pth'))

    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    testset = torchvision.datasets.CIFAR10(
        root='./data', 
        train=False,
        download=True,
        transform=transform
    )
    testloader = torch.utils.data.DataLoader(
        testset, 
        batch_size=2,
        shuffle=False, 
        num_workers=2
    )

    correct = 0
    total = 0
    combined_predictions = []
    # since we're not training, we don't need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            # calculate outputs by running images through the network
            outputs = net(images)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            combined_predictions.extend(predicted.tolist())
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')

    # save predictions CSV
    df_preds = pd.DataFrame(combined_predictions)
    df_preds.to_csv(args.preds_dir / "preds.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preds_dir",
        type=Path,
        help="Output folder containing test set predictions CSV file (preds.csv)",
    )
    parser.add_argument(
        "--train_artifacts_dir",
        type=Path,
        help="dir where trained model exists",
    )
    args = parser.parse_args()
    main(args)
