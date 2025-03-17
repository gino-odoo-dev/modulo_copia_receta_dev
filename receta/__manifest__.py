{
    'name': 'Ficha Tecnica (Receta)',
    'version': '1.0',
    'summary': 'Ingreso y Copia Ficha Tecnica',
    'description': 'modulo de Ingreso y Copia de Ficha Tecnica.',
    'author': 'Mag',
    'depends': ['base', 'mrp'],
    'data': [
        'views/receta_model_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}