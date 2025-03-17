from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FichaTecnica(models.Model):
    _inherit = 'mrp.bom' 
    _description = 'Ficha Tecnica'

    name = fields.Char(string='Nombre', required=True)
    temporadas_id = fields.Many2one('cl.product.temporadas', string='Temporadas')
    temporada_name = fields.Char(string='Nombre de Temporada', compute='_compute_temporada_name', store=True)
    articulos_id = fields.Many2one('cl.product.articulos', string='Articulos')
    articulo_name = fields.Char(string='Nombre de Articulo', compute='_compute_articulo_name', store=True)

    codigo_departamento = fields.Char(string='Codigo de Departamento', related='departamento_id.codigo', store=False, readonly=True)
    descripcion_componente = fields.Text(string='Descripcion de Componente', related='componente_id.descripcion', store=False, readonly=True)
    unidadmedida_componente = fields.Char(string='Unidad de Medida', related='componente_id.um', store=False, readonly=True)    
    descripcion_departamento = fields.Text(string='Descripcion de Departamento', related='departamento_id.descripcion', store=False, readonly=True)
    
    cantidad_id = fields.Integer(string='Cantidad', readonly=False)
    costo_unitario_id = fields.Float(string='Costo Unitario', readonly=False)
    costo_ampliado_id = fields.Float(string='Costo Ampliado', compute='calcular_costo_ampliado', store=True, readonly=True, widget="integer")
    componente_id = fields.Many2one('componente.model', string='Componente', readonly=False)
    departamento_id = fields.Many2one('departamento.model', string='Departamento', readonly=False)    
    factor_perdida_id = fields.Float(string='Factor de Perdida (%)', readonly=False)
    codigosecuencia_id = fields.Many2one('codigosecuencia.model', string='Codigo de Secuencia', readonly=False)
    compra_manufactura_id = fields.Many2one('compra_manufactura.model', string='Compra Manufactura', readonly=False)

    state = fields.Selection([('draft', 'Draft'),('next', 'Next'),('done', 'Done')], string='State', default='draft')

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('form_view'):
                nombre = record.nombre_receta if record.nombre_receta else "Articulo: Sin Nombre"
                result.append((record.id, nombre))
        return result

    @api.depends('temporadas_id')
    def _compute_temporada_name(self):
        for record in self:
            record.temporada_name = getattr(record.temporadas_id, 'name', 'Sin Temporada')

    @api.depends('articulos_id')
    def _compute_articulo_name(self):
        for record in self:
            record.articulo_name = getattr(record.articulos_id, 'name', 'Sin Articulo')

    @api.depends('cantidad_id', 'costo_unitario_id', 'factor_perdida_id')
    def calcular_costo_ampliado(self):
        for record in self:
            if record.cantidad_id and record.factor_perdida_id and record.costo_unitario_id:
                if record.factor_perdida_id > 0:
                    cantidad_perdida = (record.cantidad_id * record.factor_perdida_id) / 100
                    record.costo_ampliado_id = int(round(cantidad_perdida * record.costo_unitario_id))
                else:
                    record.costo_ampliado_id = 0
            else:
                record.costo_ampliado_id = 0

    @api.onchange('componente_id')
    def _onchange_componente_id(self):
        if self.componente_id:
            self.descripcion_componente = self.componente_id.descripcion or ''
            self.unidadmedida_componente = self.componente_id.um or ''
        else:
            self.descripcion_componente = ''
            self.unidadmedida_componente = ''

    def next_button(self):
        self.ensure_one()
        self.write({'state': 'next'})
        
        self._compute_temporada_name()
        self._compute_articulo_name()
        self.calcular_costo_ampliado()
        
        copia_ficha = self.env['copia.ficha'].search([], limit=1)
        if copia_ficha:
            copia_ficha.write({
                'part_o': self.id,
                'part_d': self.articulos_id.id,
                'temporadas_id': self.temporadas_id.id
            })
            copia_ficha._compute_temporada_name()
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fichatecnica',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {
                'default_articulos_id': self.articulos_id.id,
                'search_default_articulos_id': self.articulos_id.id,
                'default_temporadas_id': self.temporadas_id.id, 
                'default_part_o': self.id 
            },
            'domain': [('articulos_id', '=', self.articulos_id.id)],
            'views': [(self.env.ref('receta.view_receta_tree').id, 'tree'), (self.env.ref('receta.view_receta_form').id, 'form')],
        }
