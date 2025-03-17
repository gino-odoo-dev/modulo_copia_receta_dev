from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Articulos(models.Model):
    _name = 'cl.product.articulo'
    _description = 'Articulos'
    _order = 'id'
    _rec_name = 'name'

    name = fields.Char(string="Nombre", required=True)