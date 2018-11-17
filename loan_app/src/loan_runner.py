from __future__ import print_function

import argparse

from src.loan_core import LoanApp

if __name__ == "__main__":
    """
    This is main entry for the program.
    """
    # Parse input argument
    parser = argparse.ArgumentParser(description='AVLog ingest to Opus')
    parser.add_argument('--input_path', required=False, type=str, default="../large", help='Input data folder')
    parser.add_argument('--output_path', required=False, type=str, default="../small_output", help='Input data folder')
    args = parser.parse_args()

    print("Import from: {}".format(args.input_path))
    print("Result save to: {}".format(args.output_path))

    loan_app = LoanApp(args.input_path, args.output_path)

    loan_app.load_from_csv()

    loan_app.create_combine_facilities()
    loan_app.create_loan_list()

    print(loan_app.loan_list)
    print(loan_app.facilities_list)

    loan_app.process()

    print()
    print(loan_app.loan_list)
    print(loan_app.facilities_list)

    loan_app.output_to_csv()
