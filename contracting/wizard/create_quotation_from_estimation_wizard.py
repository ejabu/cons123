# -*- coding: utf-8 -*-
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import time 
import datetime

class create_quotation_from_estimation_wizard(osv.osv_memory):
    _name = "create.quotation.from.estimation.wizard"
    _description = "Create Quotation Wizard"



    def get_value_from_param(self,cr,uid,param):
        print "param>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",param
        parameter_obj = self.pool.get('ir.config_parameter')
        key =[('key', '=', param)]
        param_id = parameter_obj.search(cr,uid,key,limit=1)
        if not param_id:
            raise Warning('Parameter Not defined\nconfig it with product id and  in System Parameters with key %s'%param)
        param_obj = parameter_obj.browse(cr,uid,param_id)
        result = param_obj.value
        return int(result)
    def get_product_id(self,cr,uid,product_tmpl_id=False):
        
        product_id = self.get_value_from_param(cr,uid,param='default_product_for_estimation')
        product_obj = self.pool['product.product']
        if product_tmpl_id:
            product=product_obj.search(cr,uid,[('product_tmpl_id','=',product_tmpl_id)],limit=1)
            if product:
                product_id = product[0]
        print "product_id>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",product_id,type(product_id)
        return product_id
    def default_get(self, cr, uid, fields, context=None):
        res = super(create_quotation_from_estimation_wizard, self).default_get(cr, uid, fields, context=context)
        if context is None:
            context = {}
        active_id = context and  context.get('active_id')
        vals_material = []
        vals_lab = []
        vals_sub = []
        vals_eqp = []
        vals_log = []
        vals_mis = []
        vals = []
        if active_id:
            estimation_obj = self.pool.get('contracting.estimation').browse(cr, uid, active_id, context=context)
            if not estimation_obj.customer_id:
                raise osv.except_osv(_('Warning!'), _('define customer first'))
            res.update({'partner_id': estimation_obj.customer_id.id or False})
            for line in estimation_obj.material_line:
                product_id = line.product_id and line.product_id.id
                vals_material.append({

                    'name':line.name,

                    'product_id':self.get_product_id(cr,uid,product_tmpl_id=product_id),
                   'qty':line.qty,'product_uom':line.unit_id.id,'unit_price':line.est_amount,'purchase_price':line.rate})

            for lab_line in estimation_obj.labour_line:
                vals_lab.append({
                    'name':lab_line.name,
                    'qty':lab_line.qty,
                    'product_id':lab_line.product_id and lab_line.product_id.id or self.get_product_id(cr,uid,product_tmpl_id=False),
                    'product_uom':lab_line.unit_id.id,'unit_price':lab_line.est_amount,'purchase_price':lab_line.rate})


            for sub_line in estimation_obj.sub_cont_line:
                vals_sub.append({
                    'name':sub_line.name,
                    'qty':sub_line.qty,
                    'product_id':self.get_product_id(cr,uid,product_tmpl_id=False),
                    'product_uom':sub_line.unit_id.id,'unit_price':sub_line.est_amount,'purchase_price':sub_line.rate})


            for eqp_line in estimation_obj.eqp_line:
                vals_eqp.append(
                        {
                        'name':eqp_line.name,
                        'qty':eqp_line.qty,
                        'product_uom':eqp_line.unit_id.id,
                        'product_id':self.get_product_id(cr,uid,product_tmpl_id=False),
                        'unit_price':eqp_line.est_amount,'purchase_price':eqp_line.rate})



            for log_line in estimation_obj.log_line:
                vals_log.append({
                        'name':log_line.name,
                        'qty':log_line.qty,
                        'product_uom':log_line.unit_id.id,
                        'product_id':self.get_product_id(cr,uid,product_tmpl_id=False),
                        'unit_price':log_line.est_amount,'purchase_price':log_line.rate})


            for mis_line in estimation_obj.mis_line:
                vals_mis.append({
                    'name':mis_line.name,
                    'qty':mis_line.qty,
                    'product_id':self.get_product_id(cr,uid,product_tmpl_id=False),
                    'product_uom':mis_line.unit_id.id,
                    'unit_price':mis_line.est_amount,'purchase_price':mis_line.rate})  
            vals = vals + vals_eqp + vals_lab + vals_mis + vals_log + vals_sub + vals_material
            vals_line = []
            for val in vals:
                vals_line.append((0,0,val))
            res.update({'estimation_wizard_line': vals_line})

        return res
    def create_so(self,cr,uid,ids,context=None):
        print "DDDDDDDDDDD",context
        flag=False
        for obj in self.browse(cr,uid,ids,context):
            sale_order_id = self.pool.get('sale.order').create(cr,uid,{'partner_id':obj.partner_id.id})   
            for mat in obj.estimation_wizard_line:
              
                vals1 = {'order_id':sale_order_id,
                         'name':mat.name,
                         'product_id':mat.product_id and mat.product_id.id or self.get_product_id(cr,uid,product_tmpl_id=False),
                         'product_uom_qty':mat.qty,
                         'purchase_price':mat.purchase_price,
                         'price_unit':mat.unit_price/(mat.qty or 1),
                         'product_uom':mat.product_uom.id
                }
                flag=self.pool.get('sale.order.line').create(cr,uid,vals1)
        if flag:
            self.pool.get('contracting.estimation').write(cr,uid,context.get('active_id'),{'state':'quotation'})
        print "$$$$$$$$$$$",flag
        return True


    partner_id = fields.Many2one('res.partner', string='Customer',readonly="1")
    estimation_wizard_line = fields.One2many('create.quotation.from.estimation.wizard.line', 'estimation_wizard_id', string='Estimation Wizard Line')



class create_quotation_from_estimation_wizard_line(osv.osv_memory):
    _name = "create.quotation.from.estimation.wizard.line"
    _description = "Create Quotation Wizard Line"

    estimation_wizard_id = fields.Many2one('create.quotation.from.estimation.wizard', string='Estimation Wizard',ondelete='cascade')
    name = fields.Char('Name')
    product_id = fields.Many2one('product.product',string="Product")
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', readonly=True)
    qty = fields.Float(string='Quantity')
    unit_price = fields.Float(string='Unit Price')
    purchase_price = fields.Float(string='Cost') 


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
