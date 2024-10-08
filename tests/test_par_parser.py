"""
This module contains tests for the FWParser class in par_parser.py.
"""

import csv
import json
import logging
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add the parent directory to the Python path to import par_parser
sys.path.append(str(Path(__file__).parent.parent))

from par_parser import FWParser  # pylint: disable=wrong-import-position

# Suppress logging output during tests
logging.getLogger().setLevel(logging.ERROR)


@pytest.fixture(name="parser")
def fixture_parser():
    """
    Fixture to create a FWParser instance for testing.

    Returns:
        FWParser: An instance of FWParser with a test specification.
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as spec_file:
        spec_content = {
            "ColumnNames": ["f1", "f2", "f3"],
            "Offsets": ["5", "7", "9"],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8",
        }
        json.dump(spec_content, spec_file)
        spec_file_path = spec_file.name

    parser_instance = FWParser(spec_file_path)
    yield parser_instance
    os.unlink(spec_file_path)


def test_load_spec(parser):
    """Test that the specification is loaded correctly."""
    expected = [("f1", 5), ("f2", 7), ("f3", 9)]
    assert parser.field_specs == expected


def test_generate_fixed_width(parser):
    """Test the generation of a fixed-width file."""
    data = [{"f1": "ABC", "f2": "DEFGHIJ", "f3": "KLMNOPQRS"}]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as output_file:
        output_file_path = output_file.name

    parser.generate_fixed_width(data, output_file_path)

    with open(output_file_path, "r", encoding="windows-1252") as file:
        content = file.readlines()

    expected = ["f1   f2     f3       \n", "ABC  DEFGHIJKLMNOPQRS\n"]
    assert content == expected

    os.unlink(output_file_path)


def test_parse_fixed_width_sequential(parser):
    """Test the sequential parsing of a fixed-width file."""
    input_data = "f1   f2     f3       \nABC  DEFGHIJKLMNOPQRS\n"
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, encoding="windows-1252"
    ) as input_file:
        input_file.write(input_data)
        input_file_path = input_file.name

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as output_file:
        output_file_path = output_file.name

    parser.parse_fixed_width(input_file_path, output_file_path)

    with open(output_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    expected = [["ABC", "DEFGHIJ", "KLMNOPQRS"]]
    assert rows == expected

    os.unlink(input_file_path)
    os.unlink(output_file_path)


def test_parse_fixed_width_parallel(parser):
    """Test the parallel parsing of a fixed-width file."""
    input_data = "f1   f2     f3       \n" + ("ABC  DEFGHIJKLMNOPQRS\n" * 100)
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, encoding="windows-1252"
    ) as input_file:
        input_file.write(input_data)
        input_file_path = input_file.name

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as output_file:
        output_file_path = output_file.name

    parser.parse_fixed_width(input_file_path, output_file_path, chunk_size=10)

    with open(output_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    expected = [["ABC", "DEFGHIJ", "KLMNOPQRS"]] * 100
    assert rows == expected

    os.unlink(input_file_path)
    os.unlink(output_file_path)
