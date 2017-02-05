#-*- coding:utf-8 -*-
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.tools.translate import _

class contracting_estimation(osv.osv):
    _name = 'contracting.estimation'
    _description = 'Contracting Estimation'


    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state':'draft',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'contracting.estimation'),
        })
        return super(contracting_estimation, self).copy(cr, uid, id, default, context)

    def unlink(self,cr,uid,ids,context=None):
        for budget in self.browse(cr,uid,ids,context):
            if budget.state != 'draft':
                raise osv.except_osv(_('Integrity Error!'), _('You Can delete only Draft Estimations'))
        return super(contracting_budget, self).unlink(cr,uid,ids, context)


    def onchange_enq_no(self, cr, uid, ids,enq_id, context=None):
        res = {}
        enq_obj = self.pool.get('contracting.enquiry')
        if not enq_id:
            return res
        enq_data = enq_obj.browse(cr, uid, enq_id,context)
        value = {'customer_id':enq_data.customer_id and enq_data.customer_id.id or False,
                    'job_type_id':enq_data.job_type_id and enq_data.job_type_id.id or False,
                    'currency_id':enq_data.currency_id and enq_data.currency_id.id or False,
                    'ref':enq_data.ref or '',
                    'area': enq_data.area or '',
                    'address': enq_data.address or '',
                    'city': enq_data.city or '',
                    'state_id':enq_data.state_id and enq_data.state_id.id or False,
                    'country_id': enq_data.country_id and enq_data.country_id.id or False,
                    'submission_date':enq_data.submission_date or '',
                    
                    }
        return {'value':value}

#Override create method to include the sequence
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'contracting.estimation') or '/'
        return super(contracting_estimation, self).create(cr, uid, vals, context=context)


    def _get_total_cost(self, cr, uid, ids, field_name, arg, context=None): 
        res ={} 
        cost_material = 0
        cost_labour = 0
        sub_cost =0
        eqp_cost = 0
        log_cost =0
        mis_cost = 0
        for obj in self.browse(cr, uid, ids, context): 
            for cm in obj.material_line:
                cost_material+=cm.amount  
            for cl in obj.labour_line:
                cost_labour+=cl.amount

            for scl in obj.sub_cont_line:
                sub_cost+=scl.amount 

 
            for el in obj.eqp_line:
                eqp_cost+=el.amount

            for ll in obj.log_line:
                log_cost+=ll.amount 
 
            for ml in obj.mis_line:
                mis_cost+=ml.amount
        
            res[obj.id] = cost_material + cost_labour + sub_cost + eqp_cost + log_cost + mis_cost
        return res 

    def _get_total_margin(self, cr, uid, ids, field_name, arg, context=None): 
        res ={} 
        margin_material = 0
        margin_labour = 0
        margin_sub =0
        margin_eqp = 0
        margin_log =0
        margin_mis = 0
        for obj in self.browse(cr, uid, ids, context): 
            for cm in obj.material_line:
                margin_material+=cm.margin_amt  
            for cl in obj.labour_line:
                margin_labour+=cl.margin_amt 

            for scl in obj.sub_cont_line:
                margin_sub+=scl.margin_amt  

 
            for el in obj.eqp_line:
                margin_eqp+=el.margin_amt

            for ll in obj.log_line:
                margin_log+=ll.margin_amt
 
            for ml in obj.mis_line:
                margin_mis+=ml.margin_amt
        
            res[obj.id] = margin_material + margin_labour + margin_sub + margin_eqp + margin_log + margin_mis
        return res 


    def _get_total_estimation(self, cr, uid, ids, field_name, arg, context=None): 
        res ={} 
        estimation_material = 0
        estimation_labour = 0
        estimation_sub =0
        estimation_eqp = 0
        estimation_log =0
        estimation_mis = 0
        for obj in self.browse(cr, uid, ids, context): 
            for cm in obj.material_line:
                estimation_material+=cm.est_amount 
            for cl in obj.labour_line:
                estimation_labour+=cl.est_amount 

            for scl in obj.sub_cont_line:
                estimation_sub+=scl.est_amount  

 
            for el in obj.eqp_line:
                estimation_eqp+=el.est_amount

            for ll in obj.log_line:
                estimation_log+=ll.est_amount
 
            for ml in obj.mis_line:
                estimation_mis+=ml.est_amount
        
            res[obj.id] = estimation_material + estimation_labour + estimation_sub + estimation_eqp + estimation_log + estimation_mis
        return res 




    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

    def button_done(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'done'})
        return res







    _columns = {
        'name': fields.char('Name'),
        'enq_no': fields.many2one('contracting.enquiry','Enq Number'),
        'date': fields.date('Date',required=True),
        'customer_id': fields.many2one('res.partner','Customer',required="1"),
        'job_type_id': fields.many2one('contracting.job.type','Job Type',required=True),
        'estimator_id': fields.many2one('res.users','Estimator'),
        'submission_date': fields.date('Submission'),
        'reviewer_id': fields.many2one('res.users','Reviewer'),
        'currency_id': fields.many2one('res.currency','Currency'),
#        'revision_no': fields.char('Revision No.'),
        'ref': fields.char('Reference'),
        'description': fields.text('Description'),
        'area': fields.char('Area', size=128),
        'address': fields.char('Address', size=128),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'material_line': fields.one2many('contract.estimation.line','est_mat_id','Materials'),
        'labour_line': fields.one2many('contract.estimation.line','est_lab_id','Labour'),
        'sub_cont_line': fields.one2many('contract.estimation.line','est_sub_id','Sub'),
        'eqp_line': fields.one2many('contract.estimation.line','est_eqp_id','Eqp'),
        'distance': fields.float('Distance'),
        'start_date': fields.date('Start Date'),
        'end_date': fields.date('End Date'),
      

        'log_line': fields.one2many('contract.estimation.line','est_log_id','Log'),
        'mis_line': fields.one2many('contract.estimation.line','est_mis_id','Mis'),
        'total_cost':fields.function(_get_total_cost,string='Total Cost',type='float'), 
        'total_margin':fields.function(_get_total_margin,string='Total Margin',type='float'), 
        'total_estimation':fields.function(_get_total_estimation,string='Total Estimation',type='float'), 

        'state': fields.selection([
            ('draft', 'New'),
            ('quotation', 'Quotation Created'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
            ], 'Status', readonly=True, select=True),


       
    }
    _defaults = {
        'name': '/',
        'state':'draft',
        'date': fields.date.context_today,
    }
class contract_estimation_line(osv.osv):
    _name = "contract.estimation.line"
    _description = 'Contracting Estimation Line'



    def onchange_margin_percentage(self, cr, uid, ids, qty, rate, amount, margin,margin_amt,est_amount,context=None):
        return {'value':{'margin_amt': ((amount*margin)/100)}}

    def onchange_qty_rate_margin(self, cr, uid, ids, qty, rate, amount, margin,margin_amt,est_amount,context=None):
        res = {}
        total_amount = qty*rate 
        total_est_amount = qty*rate + margin_amt
        per_margin = 0.0
        if total_amount:
            per_margin = (margin_amt/ float(total_amount))*100
        return {'value':{'amount':total_amount,'margin':per_margin,'est_amount':total_est_amount}}


#calculate the price from bom lines
    # def onchange_bom_id(self, cr, uid, ids, bom_id,context=None):
    #     if not bom_id:
    #         return {}
    #     bom_obj = self.pool.get('mrp.bom').browse(cr, uid, bom_id,context)
    #     tax_obj = self.pool.get('account.tax')
    #     cur_obj = self.pool.get('res.currency')
    #     amount = 0.0
    #     if bom_obj.bom_line_ids:
    #         for bom_lines in bom_obj.bom_line_ids:
    #             print "????????",bom_lines.product_id.lst_price
    #             amount = amount + (bom_lines.product_id.lst_price * bom_lines.product_qty)
    #     return {'value':{'rate':amount}}


    def onchange_product_id(self,cr,uid,ids,product_id,context=None):
        if not product_id:
            return {}
        template = self.pool.get('product.template')
        temp_obj = template.browse(cr,uid,product_id,context=context)
        price = temp_obj.lst_price
        return {'value':{'rate':price}}
    def _get_budget_type(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            value = 'none'
            if record.est_mat_id:
                value= 'material'
            elif record.est_lab_id:
                value = 'labour'
            elif record.est_sub_id:
                value = 'subcontract'
            elif record.est_eqp_id:
                value = 'tools'
            elif record.est_mis_id:
                value = 'misc'
            elif record.est_log_id:
                value = 'log'

            res[record.id] = value
        return res


    @api.multi
    def onchange_cost_code(self, cost_code_id):
        if cost_code_id:
            code = self.env['cost.code'].browse(cost_code_id)
            return {'value': {'name': code.description or code.name}}
        return {}



    _columns = {
        'est_mat_id': fields.many2one('contracting.estimation','EstimateID_Mat', ondelete='cascade'),
        'est_lab_id': fields.many2one('contracting.estimation','EstimateID_Lab', ondelete='cascade'),
        'est_sub_id': fields.many2one('contracting.estimation','EstimateID_Sub', ondelete='cascade'),
        'est_eqp_id': fields.many2one('contracting.estimation','EstimateID_Eqp', ondelete='cascade'),
        'est_log_id': fields.many2one('contracting.estimation','EstimateID_Log', ondelete='cascade'),
        'est_mis_id': fields.many2one('contracting.estimation','EstimateID_Mis', ondelete='cascade'),
       


        'cost_code_id': fields.many2one('cost.code','Cost Code',required="1"),

        'timesheet_product_id': fields.many2one('product.product','Time Sheet Product'),
        'name': fields.char('Description',required=True),
        'est_details': fields.char('Details'),
        'product_id':fields.many2one('product.template',string="Product"),
        'bom_id':fields.many2one('mrp.bom','BOM'),
        'unit_id': fields.many2one('product.uom','Unit',required=True),
        'qty': fields.float('Qty'),
        'rate': fields.float('Rate'),
        'amount': fields.float('Cost'),
        'margin': fields.float('Margin%'),
        'margin_amt': fields.float('Margin'),
        'est_amount': fields.float('Estimation'),
        'partner_id':fields.many2one('res.partner','Partner',),
        'remarks':fields.char('Remarks'),

        'type': fields.function(_get_budget_type, type='selection', string='Type', store=True,
            selection= [('none','/'),
                        ('material', _('Material')),
                        ('labour', _('Labour')),
                        ('subcontract', _('Subcontract')),
                        ('misc', _('Miscellaneous')),
                        ('log', _('Logistics')),
                        ('tools', _('Tools'))]),

    }
