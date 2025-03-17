from odoo import models, fields

class Compramanufactura(models.Model):
    _name = 'compramanufactura.model'
    _description = 'Compra o Manufacturado'
    _order = 'id'
    _rec_name = 'tipo'

    tipo = fields.Char(string="Nombre", required=True)