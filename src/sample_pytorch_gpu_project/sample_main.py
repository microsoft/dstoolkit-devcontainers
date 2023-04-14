import torch


def add(x: int, y: int):
    return x + y


def main():
    print("torch.cuda.is_available():", torch.cuda.is_available())
    print("torch.cuda.device_count():", torch.cuda.device_count())
    print("torch.backends.mkl.is_available():", torch.backends.mkl.is_available())
    print("torch.backends.cudnn.is_available():", torch.backends.cudnn.is_available())
    print("torch.backends.cuda.is_built():", torch.backends.cuda.is_built())
    print("torch.backends.mkldnn.is_available():", torch.backends.mkldnn.is_available())


if __name__ == "__main__":
    main()
