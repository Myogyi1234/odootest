

{
    'name': 'student check in',
    'version': '17.0.1.0.0',
    'category': 'Education',
    'summary': 'Module for student check-in system',
    'depends': ['base','mail'],
 'data':[
     'security/ir.model.access.csv',
     'view/student_check_in_views.xml',
],
'installable': True,
    'auto_install': False,
    'application': True,
}