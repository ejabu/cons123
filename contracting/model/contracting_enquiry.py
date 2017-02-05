#-*- coding:utf-8 -*-
import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.tools.translate import _

class contracting_enquiry(osv.osv):
    _name = 'contracting.enquiry'
    _description = 'Contracting Enquiry'

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'name': self.pool.get('ir.sequence').get(cr, uid, 'contracting.enquiry'),
        })
        return super(contracting_enquiry, self).copy(cr, uid, id, default, context)

    def unlink(self,cr,uid,ids,context=None):
        if self.pool.get('contracting.estimation').search(cr,uid,[('enq_no','=',ids[0])]):
            raise osv.except_osv(_('Integrity Error!'), _('You Can delete Enquiry liked to Estimation'))
        return super(contracting_enquiry, self).unlink(cr,uid,ids, context)

#Override create method to include the sequence
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'contracting.enquiry') or '/'
        return super(contracting_enquiry, self).create(cr, uid, vals, context=context)


    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}
    
    def _get_default_stage_id(self, cr, uid, context=None):
        """ Gives default stage_id """
        stage_ids = self.pool.get('contracting.enquiry.stage').search(cr, uid, [],order='sequence', limit=1, context=context)
        if stage_ids:
            return stage_ids[0]
        return False
    

    _columns = {
        'name': fields.char('Name'),
        'date': fields.date('Date',required=True),
        'customer_id': fields.many2one('res.partner','Customer',domain=[('customer','=',True)],required=True),
        'job_type_id': fields.many2one('contracting.job.type','Job Type',required=True),
        'submission_date': fields.date('Submission'),
        'currency_id': fields.many2one('res.currency','Currency'),
        'ref': fields.char('Reference'),
        'description': fields.text('Description'),
        'area': fields.char('Area', size=128),
        'address': fields.char('Address', size=128),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'lead_id': fields.many2one('crm.lead','Opportunity'),
        'stage_id': fields.many2one('contracting.enquiry.stage', 'Stage',required=False, track_visibility='onchange'),
        'color': fields.integer('Color Index'),
        'attachment_line':fields.one2many('contracting.enquiry.attachment.line','enquiry_id','Attachment Lines'),
        }
    _defaults = {
        'name': '/',
        'color':0,
        'date': fields.date.context_today,
        'stage_id':lambda s, cr, uid, c: s._get_default_stage_id(cr, uid, c),
    }

class con_enq_attachment_line(osv.osv):
    _name = 'contracting.enquiry.attachment.line'
    _description = "Contract Enquiry Attachment"
    _columns = {
        'enquiry_id': fields.many2one('contracting.enquiry',required=True, ondelete='cascade'),
        'name': fields.char('Name',size=128,required=True),
        'attachment_type': fields.many2one('contracting.attachment.type','Attachment Type',required=True),
        'attachment':fields.binary('Attachment'),
        'description': fields.text('Description'),
    }
