import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--broadcast", action="store_true")
    parser.add_argument("-s", "--subscribe", action="store_true")
    args = parser.parse_args()
    return args
