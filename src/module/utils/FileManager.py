import json


class FileManager:

    @staticmethod
    def load_json(filepath: str):
        """Parse JSON file

        Args:
            filepath (str): The path to the JSON file.

        Raises:
            FileNotFoundError: If the file is not found.
            json.JSONDecodeError: If there's an error parsing the JSON data.

        Returns:
            object: The parsed data from the JSON file (can be a dictionary, list, etc.).

        """

        with open(filepath, "r") as file:
            try:
                data = json.load(file)
                return data
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"File not found: filepath='{filepath}'")
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(
                    f"Error parsing JSON file: error='{e}'")
