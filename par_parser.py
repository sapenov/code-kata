"""
This module provides a parser for fixed-width files with parallel processing capabilities.
"""

import csv
import json
import logging
from typing import List, Dict
from multiprocessing import Pool, cpu_count

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class FWParser:
    """
    A parser for fixed-width files with options for sequential and parallel processing.
    """

    def __init__(self, spec_file: str):
        """
        Initialize the FWParser with a specification file.

        Args:
            spec_file (str): Path to the JSON specification file.
        """
        self.spec = self.load_spec(spec_file)
        self.field_specs = list(
            zip(self.spec["ColumnNames"], map(int, self.spec["Offsets"]))
        )

    def load_spec(self, spec_file: str) -> Dict:
        """
        Load the specification from a JSON file.

        Args:
            spec_file (str): Path to the JSON specification file.

        Returns:
            Dict: The loaded specification.
        """
        with open(spec_file, "r", encoding="utf-8") as spec_file_handle:
            return json.load(spec_file_handle)

    def generate_fixed_width(self, data: List[dict], output_file: str):
        """
        Generate a fixed-width file from the given data.

        Args:
            data (List[dict]): List of dictionaries containing the data to write.
            output_file (str): Path to the output fixed-width file.
        """
        with open(
            output_file, "w", encoding=self.spec["FixedWidthEncoding"]
        ) as out_file:
            if self.spec["IncludeHeader"].lower() == "true":
                header = "".join(
                    name.ljust(int(width))
                    for name, width in zip(
                        self.spec["ColumnNames"], self.spec["Offsets"]
                    )
                )
                out_file.write(header + "\n")
            for row in data:
                line = ""
                for field, width in self.field_specs:
                    value = str(row.get(field, ""))
                    line += value.ljust(width)
                out_file.write(line + "\n")
        logging.info("Generated fixed-width file: %s", output_file)

    def parse_fixed_width(
        self, input_file: str, output_file: str, chunk_size: int = None
    ):
        """
        Parse a fixed-width file and write to a CSV file.

        Args:
            input_file (str): Path to the input fixed-width file.
            output_file (str): Path to the output CSV file.
            chunk_size (int, optional): Size of chunks for parallel processing. If None, use sequential processing.
        """
        if chunk_size:
            self.parse_fixed_width_parallel(input_file, output_file, chunk_size)
        else:
            self.parse_fixed_width_sequential(input_file, output_file)

    def parse_fixed_width_sequential(self, input_file: str, output_file: str):
        """
        Parse a fixed-width file sequentially and write to a CSV file.

        Args:
            input_file (str): Path to the input fixed-width file.
            output_file (str): Path to the output CSV file.
        """
        with open(
            input_file, "r", encoding=self.spec["FixedWidthEncoding"]
        ) as infile, open(
            output_file, "w", newline="", encoding=self.spec["DelimitedEncoding"]
        ) as outfile:
            csv_writer = csv.writer(outfile)

            if self.spec["IncludeHeader"].lower() == "true":
                next(infile)

            for line in infile:
                if line.strip():  # Skip empty lines
                    row = self.parse_line(line)
                    csv_writer.writerow(row)
        logging.info(
            "Parsed fixed-width file sequentially: %s -> %s", input_file, output_file
        )

    def parse_fixed_width_parallel(
        self, input_file: str, output_file: str, chunk_size: int
    ):
        """
        Parse a fixed-width file in parallel and write to a CSV file.

        Args:
            input_file (str): Path to the input fixed-width file.
            output_file (str): Path to the output CSV file.
            chunk_size (int): Size of chunks for parallel processing.
        """
        with open(input_file, "r", encoding=self.spec["FixedWidthEncoding"]) as infile:
            if self.spec["IncludeHeader"].lower() == "true":
                next(infile)  # Skip header
            lines = infile.readlines()

        chunks = [lines[i : i + chunk_size] for i in range(0, len(lines), chunk_size)]

        with Pool(processes=cpu_count()) as pool:
            results = pool.map(self.parse_chunk, chunks)

        with open(
            output_file, "w", newline="", encoding=self.spec["DelimitedEncoding"]
        ) as outfile:
            csv_writer = csv.writer(outfile)
            for chunk in results:
                csv_writer.writerows(chunk)
        logging.info(
            "Parsed fixed-width file in parallel: %s -> %s", input_file, output_file
        )

    def parse_chunk(self, chunk: List[str]) -> List[List[str]]:
        """
        Parse a chunk of lines from the fixed-width file.

        Args:
            chunk (List[str]): A list of lines to parse.

        Returns:
            List[List[str]]: Parsed data from the chunk.
        """
        return [self.parse_line(line) for line in chunk if line.strip()]

    def parse_line(self, line: str) -> List[str]:
        """
        Parse a single line from the fixed-width file.

        Args:
            line (str): A line from the fixed-width file.

        Returns:
            List[str]: Parsed data from the line.
        """
        row = []
        start = 0
        for _, width in self.field_specs:
            value = line[start : start + width].strip()
            row.append(value)
            start += width
        return row


if __name__ == "__main__":
    parser = FWParser("spec.json")

    # Generate sample data
    sample_data = [
        {f"f{i}": f"Value{i}" for i in range(1, 11)}
    ] * 1000  # Repeating data to create a larger dataset

    # Generate fixed-width file
    parser.generate_fixed_width(sample_data, "fixed_width.txt")

    # Parse fixed-width file to CSV (sequential)
    parser.parse_fixed_width("fixed_width.txt", "output_sequential.csv")

    # Parse fixed-width file to CSV (parallel)
    parser.parse_fixed_width("fixed_width.txt", "output_parallel.csv", chunk_size=100)

    logging.info(
        "Parsing complete. Check output_sequential.csv and output_parallel.csv for results."
    )
