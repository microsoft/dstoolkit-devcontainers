import argparse
from pathlib import Path

import mlflow
import pandas as pd
import torch
import torchvision
import torchvision.transforms as transforms
from train import Net


def main(args):
    # keep this setup code
    print("\n".join(f"{k}: {v}" for k, v in sorted(dict(vars(args)).items())))
    dict_args = vars(args)
    mlflow.autolog()
    mlflow.log_params(dict_args)

    # code below this comment is a sample only, replace with your own training code
    net = Net()
    net.load_state_dict(torch.load(args.train_artifacts_dir / "cifar_net.pth"))

    # transforms.Normalize() uses Imagenet means and stds
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    testset = torchvision.datasets.CIFAR10(
        root="./data", train=False, download=True, transform=transform
    )
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=2, shuffle=False, num_workers=2
    )

    correct = 0
    total = 0
    combined_predictions = []
    combined_labels = []
    # since we're not training, we don't need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            # calculate outputs by running images through the network
            outputs = net(images)
            # the class with the highest energy is what we choose as prediction
            predicted = torch.argmax(outputs.detach(), 1)
            combined_predictions.extend(predicted.tolist())
            combined_labels.extend(labels.tolist())
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    print(
        f"Accuracy of the network on the 10000 test images: {100 * accuracy // 1.0} %"
    )
    mlflow.log_metric("test_accuracy", accuracy)

    # save predictions CSV to output directory
    df_preds = pd.DataFrame(
        {"label": combined_labels, "prediction": combined_predictions}
    )
    df_preds.to_csv(args.preds_dir / "preds.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_artifacts_dir",
        type=Path,
        help="Directory where trained model is saved",
        default=Path("outputs"),
    )
    parser.add_argument(
        "--preds_dir",
        type=Path,
        help="Output folder containing test set predictions CSV file (preds.csv)",
        default=Path("outputs"),
    )
    args = parser.parse_args()
    main(args)
