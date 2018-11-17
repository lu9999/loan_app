from __future__ import print_function

import argparse
import copy

from src.loan_core import LoanApp

STRATEGY_OUTPUT = 0

if __name__ == "__main__":
    """
    This is main entry for the program.
    """
    # Parse input argument
    parser = argparse.ArgumentParser(description='AVLog ingest to Opus')
    parser.add_argument('--input_path', required=False, type=str, default="./small", help='Input data folder')
    parser.add_argument('--output_path', required=False, type=str, default="./small_output", help='Input data folder')
    args = parser.parse_args()

    print("Import from: {}".format(args.input_path))
    print("Result save to: {}".format(args.output_path))

    loan_app = LoanApp(args.input_path, args.output_path)

    loan_app.load_from_csv()
    loan_app.create_facilities_list()
    loan_app.create_loan_list()

    loan_result = {}
    # Run base strategy (0), from the requirement, ratio is not use here, so can give anything
    loan_result[0] = copy.deepcopy(loan_app)
    loan_result[0].process_strategy(0)
    total_profit = sum([facility.expected_yield for facility in loan_result[0].facilities_list])
    print("Strategy 0:", total_profit)

    # Run strategy (1), use expect_yield as the decision condition instead just lowest rate of facility
    loan_result[1] = copy.deepcopy(loan_app)
    loan_result[1].process_strategy(1)
    total_profit = sum([facility.expected_yield for facility in loan_result[1].facilities_list])
    print("Strategy 1:", total_profit)

    # Run strategy (2), use expect_yield / loan_amount as the decision.
    # expect_yield by itself can't really decide if the loan is worth it or not, it heavily related to the loan amount
    loan_result[2] = copy.deepcopy(loan_app)
    loan_result[2].process_strategy(2)
    total_profit = sum([facility.expected_yield for facility in loan_result[2].facilities_list])
    print("Strategy 2:", total_profit)

    # Run strategy (3), use expect_yield + ratio * (loan_amount / facility_amount) as decision condition
    # Reason: how much facility amount left is a important condition too, add extra ratio to find the best weight
    #         between 2 conditions, use ratio from 0.1 to 0.9
    for x in range(1, 11):
        loan_result[30 + x] = copy.deepcopy(loan_app)
        loan_result[30 + x].process_strategy(3, float(x)/10)

        # Analysis max profit
        max_profit = sum([facility.expected_yield for facility in loan_result[30 + x].facilities_list])
        print("Strategy 3 (ratio ", float(x)/10, ") ", max_profit)

    # output from the base strategy (Base requirement)
    loan_result[STRATEGY_OUTPUT].output_to_csv()
