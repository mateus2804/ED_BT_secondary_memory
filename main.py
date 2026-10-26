import argparse
from models import Node

parser = argparse.ArgumentParser()

parser.add_argument("input", type=str)
parser.add_argument("output", type=str)
args = parser.parse_args()

with open(args.input, 'r') as file:
    pass

print(Node(5).to_bytes())

