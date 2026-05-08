{
    'name': 'student registration',
    'version': '17.0.1.0.0',
    'category': 'Education',
    'summary': 'Module for student registration',
    'depends': ['base','mail'],
 'data':[
     'data/ir_sequence_data.xml',
     'security/ir.model.access.csv',
     'views/student_registration_view.xml',
     'views/student_parent_view.xml',
],
'installable': True,
    'auto_install': False,
    'application': True,
}