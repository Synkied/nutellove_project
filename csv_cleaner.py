# coding: utf8

import time
import multiprocessing

import pandas as pd
import dask.dataframe as dd

from constants import *


class CSVCleaner():

    def __init__(self, file_name):
        # disable SettingWithCopyWarning
        pd.options.mode.chained_assignment = None  # default='warn'
        self.file_name = file_name

    def csv_reading(self, headers, categories=[], countries=[], nutriments=[]):
        """
        Reads the csv passed to the instanciation of the class.
        headers: a list of headers that must be in the file.
        Optionals:
        categories: a list of categories to keep in the csv
        countries: a list of countries to filter the csv

        :rtype: dd.DataFrame
        """
        fname = self.file_name

        print("Cleaning CSV file... Please wait...")

        dtypes = {
            'code': 'object',
            'created_t': 'object',
            'last_modified_t': 'object',
            'cities': 'object',
            'allergens_fr': 'object',
            'cities_tags': 'object',
            'emb_codes': 'object',
            'emb_codes_tags': 'object',
            'first_packaging_code_geo': 'object',
            'generic_name': 'object',
            'ingredients_from_palm_oil_tags': 'object',
            'origins': 'object',
            'origins_tags': 'object',
            'stores': 'object',
            'serving_quantity': 'object',
        }

        start = time.time()
        # reads the specified file.
        # sep: csv file's separator
        # low_memory: avoiding unnecessary warning msgs
        csv_file = dd.read_csv(
            fname,
            sep="\t",
            encoding="utf-8",
            thousands=',',
            low_memory=False,
            dtype=dtypes,
            blocksize=25e6,
        )

        # defines a dataframe, from the passed headers
        df = csv_file[headers]

        # structures the new file to create
        # selects only specified parameters (eg. categories, countries)
        # drops products that have no name.
        new_f = df.loc[
            df['main_category_fr'].isin(categories) &
            df['countries_fr'].isin(countries) &
            df['product_name'].notnull() &
            df['nutrition_grade_fr'].notnull()
        ]

        # set nutri_grade to lower case, just in case
        new_f['nutrition_grade_fr'] = new_f['nutrition_grade_fr'].str.lower()

        end = time.time()

        print(end - start, "elapsed.")

        return new_f

    def output_to_csv(self, csv_file):

        start = time.time()

        # save the new file to a csv file, with the name "db_file.csv"
        csv_file.compute().to_csv(
            "db_file.csv",
            index=False,
            encoding="utf-8",
            sep=";",
        )

        end = time.time()

        print(end - start, "elapsed.")


if __name__ == "__main__":

    new_csv = CSVCleaner("fr.openfoodfacts.org.products.csv")

    # concatening headers + nutriments to have a seaparate list for each,
    # but having them both in the resulting csv file
    csv_file = new_csv.csv_reading(
        HEADERS_LIST + NUTRIMENTS_LIST,
        CATEGORIES_LIST,
        COUNTRIES_LIST
    )

    new_csv.output_to_csv(csv_file)
