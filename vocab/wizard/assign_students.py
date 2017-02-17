
from openerp.osv import fields, osv
from openerp.tools import float_compare
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class assign_students_wizard(osv.osv_memory):
    _name = "assign.students.wizard"

    _columns = {
        'era_id': fields.many2one('mahad.era', 'Era', required=True),
        # 'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        # 'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        # 'location_id': fields.many2one('stock.location', 'Location', required=True),
        # 'restrict_lot_id': fields.many2one('stock.production.lot', 'Lot'),
    }
    def assign_grade(self, cr, uid, ids, context=None):
        import ipdb; ipdb.set_trace()
        era_id = self.browse(cr,uid,ids).era_id.id
        student_ids = self.pool.get('mahad.student').search(cr, uid, [("era_id","=",era_id)])
        student_tuples = []
        for student_id in student_ids:
            this_tuple = (0,0,{'student_id':student_id})
            student_tuples.append(this_tuple)
        # self.pool.get('vocab.quiz').write(cr, uid, context['active_id'], {'task_ids':[(0,0,{'student_id':student_ids[0]})]} )
        self.pool.get('vocab.quiz').write(cr, uid, context['active_id'], {'task_ids':student_tuples} )


        # import ipdb; ipdb.set_trace()
        return
