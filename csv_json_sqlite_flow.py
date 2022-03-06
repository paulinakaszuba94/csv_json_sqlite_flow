import pandas as pd
import numpy as np
from datetime import datetime
from pandasql import sqldf
import sqlite3 as sq
import glob
import os

pd.options.display.float_format = '{:.2f}'.format


def load_csv_file(path: str) -> pd.DataFrame:
    """ Read csv files in a DatFrame """

    all_files = glob.glob(os.path.join(path, "*.csv"))  # Find all csv files
    df = pd.concat((pd.read_csv(open(f, 'r'), delimiter=';') for f in all_files), ignore_index=True)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ Rename columns """

    df = df.rename(columns= {'Nazwa beneficjenta pomocy': 'name',
                             'NIP beneficjenta': 'nip',
                             'Podmiot udzielający pomocy': 'support_granting_entity',
                             'Ustawa': 'act',
                             'Numer środka pomocowego': 'support_measure_number',
                             'Dzień udzielenia pomocy': 'support_day',
                             'Wielkość beneficjenta': 'beneficiary_size',
                             'Identyfikator terytorialny siedziby beneficjenta': 'beneficiary_territorial_id',
                             'Klasa PKD': 'pkd',
                             'Wartość nominalna pomocy [PLN]': 'support_nominal_value_pln',
                             'Wartość pomocy brutto [PLN]': 'support_gross_value_pln',
                             'Wartość pomocy brutto [EURO]': 'support_gross_value_eur',
                             'Forma pomocy': 'support_form',
                             'Przeznaczenie pomocy': 'support_purpose'})
    return df


def convert_str_to_float(df: pd.DataFrame, col_names: list) -> pd.DataFrame:
    """ Clean columns with money to show properly float data """

    for col_name in col_names:
        df[col_name] = [float(str(val).replace(' ', '').replace(',', '.')) for val in df[col_name].values]
    return df


def handle_missing_nip(df: pd.DataFrame) -> pd.DataFrame:
    """ Replace missing NIP (0 or null) by Name to have a clear identifier """

    df['nip_or_name'] = np.where(((df['nip'] == 0) | (df['nip'].isnull())), df['name'], df['nip'])
    return df


def make_json(df: pd.DataFrame):
    """ Convert a DataFrame to a JSON file and save this file """

    number_of_pages = int(df.shape[0] / 30)
    numbers = ""
    for i in range(1, number_of_pages+1):
        numbers += "_"
        numbers += str(i)

    todays_date = datetime.today().strftime('%Y-%m-%d')
    json_file_path = f"uokik_{todays_date}_pages{numbers}.json"

    with open(json_file_path, 'w', encoding='utf-8') as f:
        f.write(df.to_json(orient='records', lines=True, force_ascii=False))

    return json_file_path


def calc_total_support_value(df: str, col_name_to_sum: str, save=False) -> pd.DataFrame:
    """ Calculate total support value based on a specific column """

    q = f"""SELECT nip_or_name, SUM({col_name_to_sum}) AS total_support
    FROM {df} GROUP BY nip_or_name ORDER BY total_support DESC"""

    df_total = sqldf(q)

    if save:
        name_to_save = f'total_{col_name_to_sum}.xlsx'
        df_total.to_excel(name_to_save, index=False, encoding='cp1250')

    return df_total


def create_db_from_json(json_file_path: str, table_name: str, col_name_to_sum: str):
    """ Create sqlite DB based on json file.
     Create View to save a specific query."""

    df_json = pd.read_json(json_file_path, lines=True) # Read json file
    conn = sq.connect('{}.sqlite'.format(table_name)) # Create sqlite file
    df_json.to_sql(table_name, conn, if_exists='replace', index=False) # Write df to sqlite file

    cur = conn.cursor()
    # Prepare query to create a view
    q = f""" CREATE VIEW IF NOT EXISTS total_support AS 
    SELECT nip_or_name, SUM({col_name_to_sum}) AS total_support
    FROM {table_name}
    GROUP BY nip_or_name
    ORDER BY total_support DESC"""
    cur.execute(q) # Execute query
    conn.close() # Close connection



if __name__ == '__main__':

    # Load csv files and create DataFrame
    csv_path = r'C:\Users\pauli\PycharmProjects\DB' # Use your path
    df_beneficiaries = load_csv_file(csv_path)

    # Rename columns within DataFrame
    df_beneficiaries = rename_columns(df_beneficiaries)

    # Process columns that contain amounts of money
    cols_to_be_converted = ['support_nominal_value_pln', 'support_gross_value_pln', 'support_gross_value_eur']
    df_beneficiaries = convert_str_to_float(df_beneficiaries, cols_to_be_converted)

    # Handle missing/ 0 NIP values
    df_beneficiaries = handle_missing_nip(df_beneficiaries)

    # Prepare json file
    json_path = make_json(df_beneficiaries)

    # Calculate total support value
    # Choose an appropriate column to sum: 'support_nominal_value_pln', 'support_gross_value_pln', 'support_gross_value_eur'
    df_total_support = calc_total_support_value('df_beneficiaries', 'support_nominal_value_pln', save=True)

    # Create sqlite DB based on json file
    # Create VIEW that shows total support value
    # Choose an appropriate column to sum: 'support_nominal_value_pln', 'support_gross_value_pln', 'support_gross_value_eur'
    create_db_from_json(json_path, 'beneficiaries', 'support_nominal_value_pln')
