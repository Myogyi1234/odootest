{
    'name': 'for sale module',
    'version': '17.0.1.0.0',
    'summary': 'Sales',
    'description': """
        Long description here
    """,
    'category': 'Uncategorized',
    'author': 'Myo Win Aung',
    'depends': ['base', 'sale', 'sale_management'],
    'data': [
        'views/sale_order_line_views.xml',
        'views/sale_order_views.xml',
        'views/sale_menu_hide.xml',
        'views/sale_order_line_menu.xml',

    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
