# -*- coding: utf-8 -*-
import xlsxwriter
import base64
import xlrd
import os
import hashlib

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from io import BytesIO

import logging

_l = logging.getLogger(__name__)


class ImportProductBulk(models.TransientModel):
    _name = 'import.product.bulk'
    _description = 'Import Product Bulk'

    wbf = {}

    excel_file = fields.Binary(string='Excel Template')
    excel_upload = fields.Binary(string='Upload Data')

    def add_workbook_format(self, workbook):
        self.wbf['header'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#00b0f0', 'font_color': '#000000'})
        self.wbf['header'].set_border()
        self.wbf['header'].set_align('vcenter')

        self.wbf['header_style2'] = workbook.add_format(
            {'bold': 1, 'align': 'left', 'bg_color': '#00b0f0', 'font_color': '#000000'})
        self.wbf['header_style2'].set_border()
        self.wbf['header_style2'].set_align('vcenter')
        return workbook

    def download_template(self):
        """"""
        # process report excel
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        workbook = self.add_workbook_format(workbook)
        wbf = self.wbf

        worksheet = workbook.add_worksheet('Product Bulk Upload')
        worksheet.set_column(0, 0, 2)
        worksheet.set_column(0, 1, 1)
        worksheet.set_column(0, 2, 25)
        worksheet.set_column(0, 3, 25)
        worksheet.set_column(0, 4, 15)
        worksheet.set_column(0, 5, 25)

        filename = 'Product Bulk Upload' + '.xlsx'

        worksheet.write(0, 0, 'Internal Reference', wbf['header'])
        worksheet.write(0, 1, 'Barcode', wbf['header_style2'])
        worksheet.write(0, 2, 'Name', wbf['header_style2'])
        worksheet.write(0, 3, 'Cost', wbf['header_style2'])
        worksheet.write(0, 4, 'Sales Price', wbf['header_style2'])
        worksheet.write(0, 5, 'Tracking', wbf['header_style2'])

        workbook.close()
        self.excel_file = base64.encodebytes(fp.getvalue())
        fp.close()

        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=import.product.bulk&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename),
            'target': 'new'
        }

    def _get_dir_temp(self, dirname):
        a1 = os.path.split(os.path.realpath(__file__))
        a2 = os.path.split(a1[0])
        a3 = os.path.split(a2[0])
        getTemp = os.path.join(a3[0], dirname)
        if os.path.exists(getTemp) == False:
            os.mkdir(getTemp)
        return getTemp

    def _write_new_file_from_db(self, tempDir, kontent, namafile):
        pathbaru = os.path.join(tempDir, namafile)
        try:
            teks = base64.b64decode(kontent)
            newfile = open(pathbaru, 'xb')
            newfile.write(teks)
            newfile.close()
        except:
            raise UserError('error I/O file')
        return pathbaru

    def upload_template(self):
        if not self.excel_upload:
            raise UserError('File Not Selected')
        else:
            kontent = str(self.excel_upload)
            namafile = hashlib.sha256(kontent.encode()).hexdigest()
            getTemp = self._get_dir_temp('data')
            filebaru = self._write_new_file_from_db(getTemp, self.excel_upload, namafile)
            if os.path.isfile(filebaru):
                wb = xlrd.open_workbook(filebaru)
                sheet = wb.sheet_by_index(0)
                os.remove(filebaru)
                max_row = sheet.nrows
                baris = 2
                if baris >= max_row:
                    raise UserError("Please check the upload file format again, make sure there is a product value "
                                    "record in the excel row.")
                while baris < max_row:
                    new_records = []
                    updated_records = []
                    error_records = []  # To store error records
                    for baris in range(2, max_row):
                        internal_reference = sheet.cell_value(baris, 0)
                        barcode = sheet.cell_value(baris, 1)
                        name = sheet.cell_value(baris, 2)
                        cost = float(sheet.cell_value(baris, 3) or 0.0)
                        sales_price = float(sheet.cell_value(baris, 4) or 0.0)
                        tracking = sheet.cell_value(baris, 5)

                        # Check if internal_reference is null or false in a specific cell
                        if not internal_reference:
                            error_records.append(f"Error in row {baris + 1}: Internal reference is missing or false.")
                            continue

                        # Check if tracking is false because mandatory field in odoo
                        if not tracking:
                            error_records.append(f"Error in row {baris + 1}: Tracking is false.")
                            continue

                        # Check if a product with the same internal reference exists
                        existing_product = self.env['product.template'].search(
                            [('default_code', '=', internal_reference)],
                            limit=1)

                        if existing_product:
                            # Update existing product
                            existing_product.write({
                                'barcode': barcode,
                                'name': name,
                                'standard_price': cost,
                                'list_price': sales_price,
                                'tracking': tracking,
                            })
                            updated_records.append(existing_product)
                        else:
                            # Create a new product
                            new_product = self.env['product.template'].create({
                                'default_code': internal_reference,
                                'barcode': barcode,
                                'name': name,
                                'standard_price': cost,
                                'list_price': sales_price,
                                'tracking': tracking,
                            })
                            new_records.append(new_product)
                    if error_records:
                        # Raise an error with details of the issues in the Excel data
                        error_msg = "\n".join(error_records)
                        raise UserError(error_msg)

                    msg = (f'Import Successful. {len(new_records)} Product created and {len(updated_records)}'
                           f' Product updated.')
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'success',
                            'message': _(msg),
                            'next': {'type': 'ir.actions.act_window_close'},
                        }
                    }
