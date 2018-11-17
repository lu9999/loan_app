
import csv
import os

from src.covenant import Covenant
from src.facility import Facility
from src.loan import Loan


class LoanApp:
    def __init__(self, input_path, output_path):
        self.facilities_list = []
        self.loan_list = []
        self.input_path = input_path
        self.output_path = output_path
        print("Import from: {}".format(input_path))
        print("Result save to: {}".format(output_path))

        self.csv_facilities_list = []
        self.csv_covenants_list = []
        self.csv_loans_list = []

    @staticmethod
    def __load_csv_file(reader):
        title = None
        return_list = []
        for row in reader:
            if not title:
                title = row
                continue

            current_dict = {}
            for key, val in zip(title, row):
                current_dict[key] = val
            return_list.append(current_dict)
        return return_list

    def create_combine_facilities(self):
        for facility in self.csv_facilities_list:
            covenants_list = [covenant for covenant in self.csv_covenants_list
                              if covenant["bank_id"] == facility["bank_id"] and covenant["facility_id"] == facility["id"]]
            covenant = Covenant()
            for x in covenants_list:
                covenant.add_banned_state(x["banned_state"])
                covenant.add_max_default_likelihood(x["max_default_likelihood"])

            combine_facility = Facility(facility["id"],
                                        facility["amount"],
                                        facility["interest_rate"],
                                        facility["bank_id"],
                                        covenant)
            self.facilities_list.append(combine_facility)
            self.facilities_list.sort(key=lambda r: r.interest_rate)

    def create_loan_list(self):
        for loan in self.csv_loans_list:
            combine_loan = Loan(loan["id"],
                                loan["interest_rate"],
                                loan["amount"],
                                loan["default_likelihood"],
                                loan["state"])
            self.loan_list.append(combine_loan)
            self.loan_list.sort(key=lambda r: r.id)

    def process(self):
        for loan in self.loan_list:
            for facility in self.facilities_list:
                if facility.add_new_loan(loan):
                    loan.set_facility_id(facility.id)
                    break

    def load_from_csv(self):
        # Read files
        try:
            with open(os.path.join(self.input_path, "facilities.csv"), 'rb') as fh_facilities:
                facilities_reader = csv.reader(fh_facilities, delimiter=',', quotechar='|')
                self.csv_facilities_list = LoanApp.__load_csv_file(facilities_reader)

            with open(os.path.join(self.input_path, "covenants.csv"), 'rb') as fh_covenants:
                covenants_reader = csv.reader(fh_covenants, delimiter=',', quotechar='|')
                self.csv_covenants_list = LoanApp.__load_csv_file(covenants_reader)

            with open(os.path.join(self.input_path, "loans.csv"), 'rb') as fh_loans:
                loans_reader = csv.reader(fh_loans, delimiter=',', quotechar='|')
                self.csv_loans_list = LoanApp.__load_csv_file(loans_reader)
        except:
            raise Exception("Input files are incorrect.")

    def output_to_csv(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        with open(os.path.join(self.output_path, "assignments.csv"), 'wb') as fh_assignments:
            assignments_writer = csv.writer(fh_assignments, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            assignments_writer.writerow(["loan_id", "facility_id"])
            for x in filter(lambda r: r.facility_id, self.loan_list):
                assignments_writer.writerow([x.id, x.facility_id])

        with open(os.path.join(self.output_path, "yields.csv"), 'wb') as fh_yields:
            yields_writer = csv.writer(fh_yields, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            yields_writer.writerow(["facility_id", "expected_yield"])
            for x in self.facilities_list:
                yields_writer.writerow([x.id, round(x.expected_yield)])



