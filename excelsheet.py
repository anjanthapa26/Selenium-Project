from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
list_of_headers = ['Company','Designation','Responsible Person','Emails','Tech stack','Experience','Salary','Source Link']

destination_file ="./sheets/devops.xlsx"
def get_the_header_section(headers):
    wb = Workbook()
    ws = wb.active
    ft = Font(bold=True)
    for idx,header in enumerate(headers):
        ws.cell(row= 1,column=idx+1).value = headers[idx]
        ws.cell(row=1,column=idx+1).font = ft
        ws.column_dimensions[get_column_letter(idx+1)].width = 50
    return wb

wb = get_the_header_section(list_of_headers)

''' Exract the info of the table to the excel sheet '''

def extract_info_to_excel_sheet(ws,three_details_of_company,list_of_companiesDetails):
    duplicate_company_checker_list = list(map(lambda cell:cell.value,ws[get_column_letter(1)]))[1:]
    print('Got inside extract info to excel sheet section',duplicate_company_checker_list)
    if list_of_companiesDetails[0] in duplicate_company_checker_list:
        return ws
    else:
        for rows in three_details_of_company:
            print(three_details_of_company,list_of_companiesDetails)
            ws.append([list_of_companiesDetails[0],rows[0],rows[1],rows[2],list_of_companiesDetails[4],list_of_companiesDetails[1],list_of_companiesDetails[2],list_of_companiesDetails[3]])

        return ws

wb.save(filename=destination_file)






