from argparse import ArgumentParser

from game import SnakeGame

def main():
    parser = ArgumentParser(prog='snake', description='Snake Game')
    parser.add_argument('-f', '--food', help='Number of food items', type=int, default=3)
    namespace = parser.parse_args()
    SnakeGame(namespace.food).run()

if __name__ == "__main__":
    exit(main())