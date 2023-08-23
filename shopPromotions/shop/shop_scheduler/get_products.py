from .parse_zakaz import parse_zakaz
from .parse_silpo import parse_silpo
from .config import time_counter


@time_counter
def parse_manager():
    # Get products from zakaz.ua
    parse_zakaz()

    # Get products from Silpo
    parse_silpo()
