# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class mahad_student(osv.osv):

    _name = 'mahad.student'
    _description = 'Database of Student'
    _columns = {
        'name': fields.char(string='Name', required='true'),
        'nick': fields.char(string='Nick', required='true'),
        'nim': fields.char(string='NIM', required='true'),
        'era_id': fields.many2one('mahad.era', 'Era', required='true'),
        'class_id': fields.many2one('mahad.class', 'Class', required='true'),
        'user_id': fields.many2one('res.users', 'Related User', required='true'),
    }
    _defaults = {
        'nick': 'fulan',
    }
class mahad_era(osv.osv):

    _name = 'mahad.era'
    _description = 'Database of Student Era'
    _columns = {
        'name': fields.char(string='Current Grade'),
        'era': fields.char(string='Era'),
        'year_enter': fields.integer(string='Year Enter'),
    }
class mahad_class(osv.osv):

    _name = 'mahad.class'
    _description = 'Database of Student Class'
    _columns = {
        'name': fields.char(string='Class'),
    }
