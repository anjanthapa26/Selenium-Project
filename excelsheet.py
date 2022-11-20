from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

def get_the_header_section(headers):
    wb = Workbook()
    ws = wb.active
    ft = Font(bold=True)
    for idx,header in enumerate(headers):
        ws.cell(row= 1,column=idx+1).value = headers[idx]
        ws.cell(row=1,column=idx+1).font = ft
        ws.column_dimensions[get_column_letter(idx+1)].width = 50
    return [wb,ws]

''' Exract the info of the table to the excel sheet '''

def extract_info_to_excel_sheet(ws,three_details_of_company,list_of_companiesDetails):
    for rows in three_details_of_company:
        ws.append([list_of_companiesDetails[0],rows[0],rows[1],rows[2],0,list_of_companiesDetails[1],list_of_companiesDetails[2],list_of_companiesDetails[3]])
    
    return ws

def save_file(wb):
    wb.save(testsheet.xlsx)



