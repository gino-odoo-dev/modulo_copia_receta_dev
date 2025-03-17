from odoo import models, fields

class Secuencia(models.Model):
    _name = 'secuencia.model'
    _description = 'Codigo Secuencia'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Secuencia', required=True)