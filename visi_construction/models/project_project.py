# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
import openerp.addons.decimal_precision as dp



class project_project(models.Model):

    _inherit= "project.project"

    markup_amt=fields.Char(string='Markup cost', required=True, digits_compute=dp.get_precision('Product Price'))
    estimated_cost=fields.Char(string='Estimated cost', digits_compute=dp.get_precision('Product Price'))
    planned_hours=fields.Char(string='planned_hours')
    effective_hours=fields.Char(string='effective_hours')
    total_hours=fields.Char(string='total_hours')

    sale_ids = fields.One2many('sale.order', 'project_id', 'Sale Order', readonly=True)
    purchase_ids = fields.One2many('purchase.order', 'project_id', 'Purchase Order', readonly=True)
    task_ids = fields.One2many('project.task', 'project_id', 'Tasks', readonly=True)
    boq_ids = fields.One2many('boq.info', 'project', 'Boq Info', readonly=True)
    product_used_ids = fields.One2many('project.inventory.info', 'project_id', 'Product Used', readonly=True)


class sale_order_visi(models.Model):
    _inherit= "sale.order"

    project_id = fields.Many2one('project.project', 'Project')

class purchase_order_visi(models.Model):
    _inherit= "purchase.order"

    project_id = fields.Many2one('project.project', 'Project')


class project_inventory_info(models.Model):

    _name= "project.inventory.info"

    project_id = fields.Many2one('project.project', 'Project')

    inventory_id=fields.Char(string='Inventory')
    product_id = fields.Many2one('product.product', 'Product')
    estimated_qty=fields.Char(string='Estimated Qty')
    usage_qty=fields.Char(string='Usage Qty')
    consumed_qty=fields.Char(string='Consumed Qty')
