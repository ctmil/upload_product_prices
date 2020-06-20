# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import csv
from datetime import date as dt
import logging

_logger = logging.getLogger(__name__)


class ProductUploadPrices(models.Model):
    _name = 'product.upload.prices'
    _description = 'product.upload.prices'

    def btn_process(self):
        self.ensure_one()
        if not self.delimiter:
            raise ValidationError('Debe ingresar el delimitador')
        if not self.product_file:
            raise ValidationError('Debe seleccionar el archivo')
        if self.state != 'draft':
            raise ValidationError('Archivo procesado!')
        self.file_content = base64.decodestring(self.product_file)
        lines = self.file_content.split('\n')
        for line in lines:
            lista = line.split(self.delimiter)
            if len(lista) == 3:
                default_code = lista[0]
                list_price = float(lista[1])
                standard_price = float(lista[2])
                product = self.env['product.template'].search([('default_code','=',default_code)])
                if product:
                    product.list_price = list_price
                    product.standard_price = standard_price
                else:
                    not_processed_content = self.not_processed_content or '' + line or '' + '\n'
                    self.not_processed_content = not_processed_content
            else:
                not_processed_content = self.not_processed_content or '' + line or '' + '\n'
                self.not_processed_content = not_processed_content

        self.state = 'processed'

    name = fields.Char('Nombre')
    product_file = fields.Binary('Archivo')
    delimiter = fields.Char('Delimitador',default=",")
    state = fields.Selection(selection=[('draft','Borrador'),('processed','Procesado')],string='Estado',default='draft')
    file_content = fields.Text('Texto archivo')
    not_processed_content = fields.Text('Texto no procesado')
