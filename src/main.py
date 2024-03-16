import sys
from module import FirstFacade


def read_formatteds() -> list[str]:
    input_filename = sys.argv[1]
    with open(input_filename, 'r') as f:
        formatteds = f.read()
    return formatteds


if __name__ == '__main__':
    formatteds = read_formatteds()
    completed_formatteds = FirstFacade.calculate_shipment(formatteds)
    print(completed_formatteds)
