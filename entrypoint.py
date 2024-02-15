from config.base import TOTAL_DATASETS_TO_GENERATE
from src import main_routine


def main():
    for _ in range(TOTAL_DATASETS_TO_GENERATE):
        main_routine.start()


if __name__ == "__main__":
    main()
