from argparse import ArgumentParser

from game import SnakeGame

def main():
    parser = ArgumentParser(prog='snake', description='Snake Game')
    parser.add_argument('-f', '--food', help='Number of food items', type=int, default=3)
    parser.add_argument('-s', '--server', help='Server address', type=str, default='localhost:8080')
    namespace = parser.parse_args()
    SnakeGame(namespace.food, namespace.server).run()

if __name__ == "__main__":
    exit(main())