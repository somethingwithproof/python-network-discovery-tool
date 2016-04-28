import openpyxl
import datetime
from device import Device
import mail


def today():
    return str(datetime.date.today())


def import_from_excel(spreadsheet):
    # open xls and get input sheet
    wb = openpyxl.load_workbook(spreadsheet)
    sheets = wb.get_sheet_names()

    sheet = wb.get_sheet_by_name(sheets[0])

    devices = []

    for row in range(2, sheet.max_row + 1):
        # Each row in the spreadsheet has data for one device.
        host = sheet['A' + str(row)].value
        ip = sheet['C' + str(row)].value
        snmp_group = sheet['D' + str(row)].value
        mysql_user = sheet['I' + str(row)].value
        mysql_password = sheet['J' + str(row)].value

        device = Device(row - 1, host, ip, snmp_group,
                        mysql_user=mysql_user, mysql_password=mysql_password)
        devices.append(device)

    return devices


def assign_open_closed(sheet, column, row, value):
    if value:
        sheet[column + str(row)] = 'open'
    else:
        sheet[column + str(row)] = 'closed'


def export_to_excel(devices, spreadsheet=None):
    if spreadsheet is None:
        wb = openpyxl.Workbook()
        sheets = wb.get_sheet_names()

        sheet = wb.get_sheet_by_name(sheets[0])
    else:
        wb = openpyxl.load_workbook(spreadsheet)
        wb.create_sheet(title=today() + '_check')

        sheet = wb.get_sheet_by_name(today() + '_check')

    sheet['A1'] = 'name'
    sheet['B1'] = 'managementip'
    sheet['C1'] = 'state'
    sheet['D1'] = 'snmp'
    sheet['E1'] = 'ssh'
    sheet['F1'] = 'mysql'
    sheet['G1'] = 'errors'

    for idx, device in enumerate(devices):
        sheet['A' + str(idx + 2)] = device.host
        sheet['B' + str(idx + 2)] = device.ip

        if device.alive:
            sheet['C' + str(idx + 2)] = 'up'
        else:
            sheet['C' + str(idx + 2)] = 'down'

        assign_open_closed(sheet, 'D', idx + 2, device.snmp)
        assign_open_closed(sheet, 'E', idx + 2, device.ssh)
        assign_open_closed(sheet, 'F', idx + 2, device.mysql)

        sheet['G' + str(idx + 2)] = device.errors

    wb.save(today() + '_check.xlsx')

    if spreadsheet is not None:
        try:
            mail.send(today() + '_check.xlsx')
        except:
            print "Error sending mail(s)"
