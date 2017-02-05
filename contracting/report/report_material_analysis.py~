# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv
class report_material_analysis_view(osv.osv):
    _name = "report.material.analysis.view"
    _description = "Material Analysis"
    _auto = False
    _rec_name = 'analytic_id'
    _columns = {
        'analytic_id': fields.many2one('account.analytic.account','Analytic',readonly=True),
        'partner_id': fields.many2one('res.partner','Partner',readonly=True),
        'origin': fields.char('Source Document',readonly=True),

        'stat': fields.selection([('draft', 'Draft'),('cancel', 'Cancelled'),
                ('waiting', 'Waiting Another Operation'),
                ('confirmed', 'Waiting Availability'),
                ('partially_available', 'Partially Available'),
                ('assigned', 'Ready to Transfer'),
                ('done', 'Transferred'),
                ], string='Status', readonly=True),
        'date': fields.date('Date'),
        'picking_id': fields.many2one('stock.picking','Picking',readonly=True),
        'company_id':fields.many2one('res.company','Company',readonly=True),
        'product_id': fields.many2one('product.product','Product',readonly=True),
        'move_id' : fields.many2one('stock.move','Move',readonly=True),
        'location_dest_id': fields.many2one('stock.location','Destination',readonly=True),
        'location_id': fields.many2one('stock.location','Source',readonly=True),
        'qty': fields.float('Qty',readonly=True),
        'cost': fields.float('Cost',readonly=True),

    }

    def init(self,cr):
        tools.drop_view_if_exists(cr, 'report_material_analysis_view')
        cr.execute("""create or replace view report_material_analysis_view as(
SELECT
        ROW_NUMBER () OVER (ORDER BY stock_picking.analytic_account_id ) AS id,
         stock_picking.analytic_account_id as analytic_id,
        stock_picking.partner_id as partner_id,
        stock_picking.origin as origin,
        stock_picking."state" as state,
        stock_picking."date" as date,
        stock_picking.id as picking_id,
        stock_picking.company_id as company_id,
        stock_move.product_id as product_id,
        stock_move.id as move_id,
        stock_move.location_dest_id as location_dest_id,
        stock_move.location_id as location_id,
        stock_move.product_qty as qty,
        (stock_move.product_qty*stock_move.price_unit) AS cost
FROM
        stock_picking
INNER JOIN stock_move ON stock_picking."id" = stock_move.picking_id
WHERE
        stock_picking.analytic_account_id IS NOT NULL


)""")

