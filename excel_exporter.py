import logging
from os.path import exists

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.worksheet.table import TableStyleInfo, Table
from openpyxl.worksheet.worksheet import Worksheet
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)


def prettify_excel_file(excel_file: str):
    workbook = openpyxl.load_workbook(excel_file)
    # maybe add all sheets later
    set_table_style(workbook.active, 'active_table')
    auto_fit_columns(workbook.active)
    workbook.save(excel_file)
    workbook.close()


def auto_fit_columns(worksheet: Worksheet):
    for column_cells in worksheet.columns:
        max_length = max(len(str(cell.value)) for cell in column_cells)
        min_length = len(column_cells[0].value) + 5
        worksheet.column_dimensions[column_cells[0].column_letter].width = max(min_length, max_length)


def set_table_style(worksheet: Worksheet, table_name: str, table_style: str = 'TableStyleLight16'):
    table_style = TableStyleInfo(name=table_style,
                                 showFirstColumn=False,
                                 showLastColumn=False,
                                 showRowStripes=True,
                                 showColumnStripes=False)
    worksheet.freeze_panes = 'A2'
    table = Table(displayName=table_name, ref=worksheet.dimensions)
    table.tableStyleInfo = table_style
    worksheet.add_table(table)


def excel_exporter(input_jsonl_file: str, output_excel_file: str = 'stores.xlsx'):
    if not exists(input_jsonl_file):
        return

    df = pd.read_json(input_jsonl_file, lines=True).drop_duplicates()

    column_order = ['Source', 'Name1', 'Name2', 'Gmbh', 'MapboxId', 'MapboxAddress', 'Address', 'City', 'Zip', 'Email', 'EmailDomain', 'Phone', 'Website', 'Latitude', 'Longitude']
    df = df.reindex(columns=column_order)
    df.sort_values(inplace=True, by=['Source', 'Name1'])

    df.to_excel(output_excel_file, index=False)

    prettify_excel_file(output_excel_file)


def group_by_mapbox_id(input_excel_file: str = 'stores.xlsx', output_excel_file: str = 'grouped_stores.xlsx'):
    def longest_value(series: pd.Series):
        sorted_by_length = sorted(series.tolist(), key=lambda x: len(str(x)))
        return sorted_by_length[-1]

    def shortest_value(series: pd.Series):
        sorted_by_length = sorted(series.tolist(), key=lambda x: len(str(x)))
        return sorted_by_length[0]

    def unique_values(series: pd.Series):
        return series.dropna().unique()

    df = pd.read_excel(input_excel_file)
    agg_funcs = {
        'Name1': longest_value,
        'Name2': longest_value,
        'Gmbh': shortest_value,
        'MapboxAddress': 'first',
        'Address': longest_value,
        'City': longest_value,
        'Zip': longest_value,
        'Latitude': longest_value,
        'Longitude': longest_value,
        'Source': unique_values,
        'Email': unique_values,
        'Phone': unique_values,
        'Website': unique_values,
    }

    possible_sources = set(df['Source'])

    grouped_df = df.groupby('MapboxId').agg(agg_funcs).reset_index()

    if grouped_df.empty:
        raise Exception('It seems there are no Mapbox IDs in the excel file.')

    email_series = grouped_df['Email'].apply(pd.Series).add_prefix('Email')

    for email_column in email_series.columns:
        email_series[f'{email_column}Domain'] = email_series[email_column].apply(lambda x: str(x).split('@')[-1] if pd.notna(x) else np.nan)

    website_series = grouped_df['Website'].apply(pd.Series).add_prefix('Website')
    phone_series = grouped_df['Phone'].apply(pd.Series).add_prefix('Phone')

    result_df = pd.concat([grouped_df, email_series, phone_series, website_series], axis=1)

    for source in possible_sources:
        result_df[source] = result_df['Source'].apply(lambda x: source in x)

    columns_to_delete = ['Source', 'Email', 'Phone', 'Website']
    for column in columns_to_delete:
        del result_df[column]

    result_df = result_df.replace(np.nan, '', regex=True)
    result_df.to_excel(output_excel_file, index=False)

    prettify_excel_file(output_excel_file)


def main():
    try:
        settings = get_project_settings()
        data_file = settings.get('DATA_FILE')
        excel_file = settings.get('EXCEL_FILE')
        grouped_file = settings.get('GROUPED_FILE')

        if not exists(excel_file):
            excel_exporter(data_file, output_excel_file=excel_file)

        group_by_mapbox_id(input_excel_file=excel_file, output_excel_file=grouped_file)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
