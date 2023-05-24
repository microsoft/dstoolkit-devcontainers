from sample_pytorch_gpu_project import sample_main


def test_main():
    sample_main.main()


def test_add():
    assert sample_main.add(1, 2) == 3
