from sample_cpu_project import sample_main


def test_main():
    assert sample_main.main(1, 2) == 3
