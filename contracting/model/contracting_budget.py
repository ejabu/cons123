#-*- coding:utf-8 -*-
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.tools.translate import _

class contracting_budget(osv.osv):
    _name = 'contracting.budget'
    _description = 'Contracting Budget'


    def unlink(self,cr,uid,ids,context=None):
        for budget in self.browse(cr,uid,ids,context):
            if budget.state != 'draft':
                raise osv.except_osv(_('Integrity Error!'), _('You Can delete only Draft Budgets'))
        return super(contracting_budget, self).unlink(cr,uid,ids, context)


    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state':'draft',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'contracting.budget'),
           # 'date': fields.date.context_today,
        })
        return super(contracting_budget, self).copy(cr, uid, id, default, context)

    def button_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'confirm'})

    def button_done(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'done'})
        return res




    def copy_estimate(self, cr, uid, ids, context=None):
        budget= self.browse(cr,uid,ids,context)
        copy_det_bom = budget.copy_det_bom
        budget_id = self.browse(cr,uid,ids,context) and self.browse(cr,uid,ids,context).id
        estimation_obj = budget.estimation_id
        estimation_id = budget.estimation_id and budget.estimation_id.id
        line_obj = self.pool.get('contracting.budget.line')

#material grid line
        #unlink option 
        existing_material_line_ids = self.pool.get('contracting.budget.line').search(cr,uid,[('budget_mat_id','=',budget_id)])
        self.pool.get('contracting.budget.line').unlink(cr, uid, existing_material_line_ids, context=context)    
        # creating the material grid
        for material_lines in estimation_obj.material_line:
            if copy_det_bom:
                bom_id = material_lines.bom_id
                # mbom_id  = material_lines.bom_id and material_lines.bom_id.id
                cost_code_id = material_lines.cost_code_id and material_lines.cost_code_id.id
                account_analytic_id = budget.account_analytic_id and budget.account_analytic_id.id
                name = material_lines.name
                partner_id = material_lines.partner_id and material_lines.partner_id.id
                unit_id = material_lines.unit_id and material_lines.unit_id.id
                qty = material_lines.qty
                for line in bom_id.bom_line_ids:
                    product_id = line.product_id and line.product_id.product_tmpl_id and line.product_id.product_tmpl_id.id
                    rate = line.product_id.lst_price
                    material_vals = {
                    'cost_code_id':cost_code_id,
                    'account_analytic_id': account_analytic_id,
                    'name':name,
                    'partner_id':partner_id,
                    'product_id': product_id,
                    # 'bom_id':mbom_id,
                    'unit_id':unit_id,
                    'qty':qty,
                    'rate':rate,

                    'budget_mat_id':budget_id
                    }
                    line_obj.create(cr,uid,material_vals,context)
            else:
            
                material_vals = {
                    'cost_code_id':material_lines.cost_code_id and material_lines.cost_code_id.id,
                    'account_analytic_id': budget.account_analytic_id and budget.account_analytic_id.id,
                    'name':material_lines.name,
                    'product_id':material_lines.product_id and material_lines.product_id.id,
                    'partner_id':material_lines.partner_id and material_lines.partner_id.id,
                    'bom_id':material_lines.bom_id and material_lines.bom_id.id,
                    'unit_id':material_lines.unit_id and material_lines.unit_id.id,
                    'qty':material_lines.qty,
                    'rate':material_lines.rate,
                    'budget_mat_id':budget_id
                }
                line_obj.create(cr,uid,material_vals,context)





#labour grid line
        #unlink option 
        existing_labour_line_ids = self.pool.get('contracting.budget.line').search(cr,uid,[('budget_lab_id','=',budget_id)])
        self.pool.get('contracting.budget.line').unlink(cr, uid, existing_labour_line_ids, context=context)    
        # creating the labour grid
        for labour_lines in estimation_obj.labour_line:
            labour_vals = {
                'cost_code_id':labour_lines.cost_code_id and labour_lines.cost_code_id.id,
                'account_analytic_id': budget.account_analytic_id and budget.account_analytic_id.id,
                'name':labour_lines.name,
                'partner_id':labour_lines.partner_id and labour_lines.partner_id.id,
                'unit_id':labour_lines.unit_id and labour_lines.unit_id.id,
                'qty':labour_lines.qty,
                'rate':labour_lines.rate,
                'budget_lab_id':budget_id
            }
            line_obj.create(cr,uid,labour_vals,context)




#subcontract grid line
        #unlink option 
        existing_subcontract_line_ids = self.pool.get('contracting.budget.line').search(cr,uid,[('budget_sub_id','=',budget_id)])
        self.pool.get('contracting.budget.line').unlink(cr, uid, existing_subcontract_line_ids, context=context)    
        # creating the labour grid
        for subcontract_lines in estimation_obj.sub_cont_line:
            subcontract_vals = {
                'cost_code_id':subcontract_lines.cost_code_id and subcontract_lines.cost_code_id.id,
                'account_analytic_id': budget.account_analytic_id and budget.account_analytic_id.id,
                'name':subcontract_lines.name,
                'partner_id':subcontract_lines.partner_id and subcontract_lines.partner_id.id,
                'unit_id':subcontract_lines.unit_id and subcontract_lines.unit_id.id,
                'qty':subcontract_lines.qty,
                'rate':subcontract_lines.rate,
                'budget_sub_id':budget_id
            }
            line_obj.create(cr,uid,subcontract_vals,context)


#Tools and Equipments grid line


        #unlink option 
        existing_eqp_line_ids = self.pool.get('contracting.budget.line').search(cr,uid,[('budget_eqp_id','=',budget_id)])
        self.pool.get('contracting.budget.line').unlink(cr, uid, existing_eqp_line_ids, context=context)    
        # creating the Tools and Equipments grid line
        for eqp_lines in estimation_obj.eqp_line:
            eqp_vals = {
                'cost_code_id':eqp_lines.cost_code_id and eqp_lines.cost_code_id.id,
                'account_analytic_id': budget.account_analytic_id and budget.account_analytic_id.id,
                'name':eqp_lines.name,
                'partner_id':eqp_lines.partner_id and eqp_lines.partner_id.id,
                'unit_id':eqp_lines.unit_id and eqp_lines.unit_id.id,
                'qty':eqp_lines.qty,
                'rate':eqp_lines.rate,
                'budget_eqp_id':budget_id
            }
            line_obj.create(cr,uid,eqp_vals,context)




#Logistics and Transportation grid line


        #unlink option 
        existing_log_line_ids = self.pool.get('contracting.budget.line').search(cr,uid,[('budget_log_id','=',budget_id)])
        self.pool.get('contracting.budget.line').unlink(cr, uid, existing_log_line_ids, context=context)    
        # creating the Logistics and Transportation grid line
        for log_lines in estimation_obj.log_line:
            log_vals = {
                'cost_code_id':log_lines.cost_code_id and log_lines.cost_code_id.id,
                'account_analytic_id': budget.account_analytic_id and budget.account_analytic_id.id,
                'name':log_lines.name,
                'partner_id':log_lines.partner_id and log_lines.partner_id.id,
                'unit_id':log_lines.unit_id and log_lines.unit_id.id,
                'qty':log_lines.qty,
                'rate':log_lines.rate,
                'budget_log_id':budget_id
            }
            line_obj.create(cr,uid,log_vals,context)


#MISC grid line


        #unlink option 
        existing_mis_line_ids = self.pool.get('contracting.budget.line').search(cr,uid,[('budget_mis_id','=',budget_id)])
        self.pool.get('contracting.budget.line').unlink(cr, uid, existing_mis_line_ids, context=context)    
        # creating the MISC grid line
        for mis_lines in estimation_obj.mis_line:
            mis_vals = {
                'cost_code_id':mis_lines.cost_code_id and mis_lines.cost_code_id.id,
                'account_analytic_id': budget.account_analytic_id and budget.account_analytic_id.id,
                'name':mis_lines.name,
                'partner_id':mis_lines.partner_id and mis_lines.partner_id.id,
                'unit_id':mis_lines.unit_id and mis_lines.unit_id.id,
                'qty':mis_lines.qty,
                'rate':mis_lines.rate,
                'budget_mis_id':budget_id
            }
            line_obj.create(cr,uid,mis_vals,context)


        return True



    def onchange_estimation_id(self, cr, uid, ids,est_id, context=None):
        res = {}
        est_obj = self.pool.get('contracting.estimation')
        if not est_id:
            return res
        est_data = est_obj.browse(cr, uid, est_id,context)
        res = {'value':{'customer_id':est_data.customer_id and est_data.customer_id.id or False,
                    'job_type_id':est_data.job_type_id and est_data.job_type_id.id or False,
                    'currency_id':est_data.currency_id and est_data.currency_id.id or False,
                    'area': est_data.area or '',
                    'address': est_data.address or '',
                    'city': est_data.city or '',
                    'state_id':est_data.state_id and est_data.state_id.id or False,
                    'country_id': est_data.country_id and est_data.country_id.id or False,
                    'submission_date':est_data.submission_date or '',
                    'estimator_id': est_data.estimator_id and est_data.estimator_id.id or False,
                    'reviewer_id':est_data.reviewer_id and est_data.reviewer_id.id or False,
                    'distance':est_data.distance or 0.0,
                    'start_date':est_data.start_date,
                    'end_date':est_data.end_date,
                    'ref':est_data.ref or '',
                    }
                }
        return res

#Override create methto include the sequence
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'contracting.budget') or '/'
        return super(contracting_budget, self).create(cr, uid, vals, context=context)


    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}




    _columns = {
        'name': fields.char('Name'),
        'copy_det_bom':fields.boolean('BOM Detail'),
#        'enq_no': fields.many2one('contract.enquiry','Enq Number'),
        'estimation_id': fields.many2one('contracting.estimation','Estimation'),
        'account_analytic_id': fields.many2one('account.analytic.account','Contract',required=True),

        'date': fields.date('Date',required=True),
        'customer_id': fields.many2one('res.partner','Customer',required=True),

        'job_type_id': fields.many2one('contracting.job.type','Job Type',required=True),
        'estimator_id': fields.many2one('res.users','Estimator'),
        'planned_date': fields.date('Planned Date'),
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
        'material_line': fields.one2many('contracting.budget.line','budget_mat_id','Materials'),
        'labour_line': fields.one2many('contracting.budget.line','budget_lab_id','Labour'),
        'sub_cont_line': fields.one2many('contracting.budget.line','budget_sub_id','Sub'),
        'eqp_line': fields.one2many('contracting.budget.line','budget_eqp_id','Eqp'),

        'log_line': fields.one2many('contracting.budget.line','budget_log_id','Log'),
        'mis_line': fields.one2many('contracting.budget.line','budget_mis_id','Misc'),

        'distance': fields.float('Distance'),
        'start_date': fields.date('Start Date'),
        'end_date': fields.date('End Date'),
        'state': fields.selection([
            ('draft', 'New'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
            ], 'Status', readonly=True, track_visibility='onchange',
            help="Gives the status of the Budget", select=True),

    }
    _defaults = {
        'name': '/',
        'date': fields.date.context_today,
        'state':'draft',
    }

class contracting_budget_line(osv.osv):
    _name = "contracting.budget.line"
    _description = "Contract Budget line"


    def onchange_budget_percentage(self, cr, uid, ids, qty, rate, budget_amount, budget,actual_amt,bal_amount,context=None):
        return {'value':{}}

    def onchange_qty_rate(self, cr, uid, ids, qty, rate,actual_amt,context=None):
        res = {}
        total_amount = qty*rate 
        total_bal_amount = qty*rate - actual_amt
        per_budget = 0.0
        if total_amount:
            per_budget = (actual_amt/ float(total_amount))*100
        return {'value':{'budget_amount':total_amount,'bal_amount':total_bal_amount}}


    def _get_budget_amount(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            val = 0.0
            val = line.qty * line.rate
            res[line.id] = val
        return res

    def _get_bal_amount(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            val = 0.0
            val = (line.qty * line.rate) - line.actual_amt
            res[line.id] = val
        return res

    def _get_budget_id_func(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
#            val = 0.0
#            val = line.qty * line.rate
            budget_id = line.budget_mat_id and line.budget_mat_id.id or \
                        line.budget_lab_id and line.budget_lab_id.id or \
                        line.budget_sub_id and line.budget_sub_id.id or \
                        line.budget_eqp_id and line.budget_eqp_id.id or \
                        line.budget_log_id and line.budget_log_id.id or \
                        line.budget_mis_id and line.budget_log_id.id
            res[line.id] = budget_id
        return res


#calculate the price from bom lines
    # def onchange_bom_id(self, cr, uid, ids, bom_id,context=None):
    #     if not bom_id:
    #         return {}
    #     bom_obj = self.pool.get('mrp.bom').browse(cr, uid, bom_id,context)
    #     amount = bom_obj.standard_price or 0.0
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
            if record.budget_mat_id:
                value= 'material'
            elif record.budget_lab_id:
                value = 'labour'
            elif record.budget_sub_id:
                value = 'subcontract'
            elif record.budget_eqp_id:
                value = 'tools'
            elif record.budget_mis_id:
                value = 'misc'
            elif record.budget_log_id:
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
        'budget_mat_id': fields.many2one('contracting.budget','BudgetID_Mat', ondelete='cascade'),
        'budget_lab_id': fields.many2one('contracting.budget','BudgetID_Lab', ondelete='cascade'),
        'budget_sub_id': fields.many2one('contracting.budget','BudgetID_Sub', ondelete='cascade'),
        'budget_eqp_id': fields.many2one('contracting.budget','BudgetID_Eqp', ondelete='cascade'),
        'budget_log_id': fields.many2one('contracting.budget','BudgetID_Log', ondelete='cascade'),
        'budget_mis_id': fields.many2one('contracting.budget','BudgetID_Misc', ondelete='cascade'),
        'budget_id_func': fields.function(_get_budget_id_func,string='Parent Budget', type="integer",store=True),
        'account_analytic_id': fields.many2one('account.analytic.account','Job#'),
        'parent_id':fields.many2one('contracting.budget.line','Parent'),
        'asset_id': fields.many2one('account.asset.asset','Asset'),
#        'product_id': fields.many2one('product.product','Costcode'),
        'cost_code_id': fields.many2one('cost.code','Cost Code',required="1"),
        'timesheet_product_id': fields.many2one('product.product','Time Sheet Product'),
        'name': fields.char('Description',required=True),
        'est_details': fields.char('Details'),
        'product_id':fields.many2one('product.template',string="Product"),
        'bom_id':fields.many2one('mrp.bom','BOM'),
        'unit_id': fields.many2one('product.uom','Unit'),
        'qty': fields.float('Qty'),
        'rate': fields.float('Rate'),
        'budget_amount': fields.function(_get_budget_amount,string='Amount',store=True),
       # 'amount' : fields.function(_get_amount,string='Amount'),
        'utilized': fields.float('Utl %'),
        'actual_amt': fields.float('Actual Amount'),
       # 'bal_amount': fields.float('Balance'),
        'partner_id':fields.many2one('res.partner','Partner',),
        'bal_amount': fields.function(_get_bal_amount,string='Balance',store=True),

        'type': fields.function(_get_budget_type, type='selection', string='Type', store=True,
            selection= [('none','/'),
                        ('material', _('Material')),
                        ('labour', _('Labour')),
                        ('subcontract', _('Subcontract')),
                        ('misc', _('Miscellaneous')),
                        ('log', _('Logistics')),
                        ('tools', _('Tools'))]),

    }

