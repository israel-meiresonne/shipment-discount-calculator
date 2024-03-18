import sys
from module import FirstFacade

COUNTRY = 'fr'
FILE_INPUT = 'input.txt'


def read_formatteds() -> list[str]:
    input_filename = sys.argv[1] if len(sys.argv) >= 2 else FILE_INPUT
    with open(input_filename, 'r') as file:
        lines = file.readlines()
    rows = [line.strip() for line in lines]
    return rows


if __name__ == '__main__':
    formatteds = read_formatteds()
    treated_formatteds = FirstFacade.calculate_shipment(COUNTRY, formatteds)
    for treated_formatted in treated_formatteds:
        print(treated_formatted)
