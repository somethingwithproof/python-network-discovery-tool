import openpyxl
from datetime import date
from typing import List

from device import Device
import mail


def import_from_excel(spreadsheet: str) -> List[Device]:
    # Open spreadsheet and get input sheet
    wb = openpyxl.load_workbook(spreadsheet)
    sheet = wb.active

    devices = []

    for row in range(2, sheet.max_row + 1):
        # Each row in the spreadsheet has data for one device.
        host = sheet[f'A{row}'].value
        ip = sheet[f'C{row}'].value
        snmp_group = sheet[f'D{row}'].value
        mysql_user = sheet[f'I{row}'].value
        mysql_password = sheet[f'J{row}'].value

        device = Device(row - 1, host, ip, snmp_group,
                        mysql_user=mysql_user, mysql_password=mysql_password)
        devices.append(device)

    return devices


def assign_open_closed(sheet, column, row, value):
    if value:
        sheet[f'{column}{row}'] = 'open'
    else:
        sheet[f'{column}{row}'] = 'closed'


def export_to_excel(devices: List[Device], spreadsheet: str = None):
    if spreadsheet is None:
        wb = openpyxl.Workbook()
        sheet = wb.active
    else:
        wb = openpyxl.load_workbook(spreadsheet)
        sheet_name = f'{date.today().isoformat()}_check'
        sheet = wb.create_sheet(title=sheet_name)

    sheet['A1'] = 'name'
    sheet['B1'] = 'managementip'
    sheet['C1'] = 'state'
    sheet['D1'] = 'snmp'
    sheet['E1'] = 'ssh'
    sheet['F1'] = 'mysql'
    sheet['G1'] = 'errors'

    for idx, device in enumerate(devices):
        sheet[f'A{idx + 2}'] = device.host
        sheet[f'B{idx + 2}'] = device.ip

        if device.alive:
            sheet[f'C{idx + 2}'] = 'up'
        else:
            sheet[f'C{idx + 2}'] = 'down'

        assign_open_closed(sheet, 'D', idx + 2, device.snmp)
        assign_open_closed(sheet, 'E', idx + 2, device.ssh)
        assign_open_closed(sheet, 'F', idx + 2, device.mysql)

        sheet[f'G{idx + 2}'] = device.errors

    wb.save(f'{date.today().isoformat()}_check.xlsx')

    if spreadsheet is not None:
        try:
            mail.send(f'{date.today().isoformat()}_check.xlsx')
        except Exception as e:
            print(f'Error sending email: {e}')
