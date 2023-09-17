import logging
from os.path import exists

import openpyxl
import pandas as pd
from openpyxl.worksheet.table import TableStyleInfo, Table
from openpyxl.worksheet.worksheet import Worksheet

logger = logging.getLogger(__name__)


def auto_fit_columns(worksheet: Worksheet):
    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = min(100, length * 1.33 + 5)


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

    column_order = ['Source', 'Name1', 'Name2', 'Address', 'City', 'Zip', 'Email', 'Phone', 'Website', 'Latitude', 'Longitude']
    df = df.reindex(columns=column_order)
    df.sort_values(inplace=True, by=['Source', 'Name1'])

    df.to_excel(output_excel_file, index=False)

    workbook = openpyxl.load_workbook(output_excel_file)
    set_table_style(workbook.active, 'stores')
    auto_fit_columns(workbook.active)
    workbook.save(output_excel_file)
    workbook.close()
