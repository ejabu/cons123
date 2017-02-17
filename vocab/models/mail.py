from openerp import models, fields, api, _
from email.utils import formataddr

class mail_message(models.Model):
    _inherit= "mail.message"

    @api.v7
    def _get_default_from(self, cr, uid, context=None):
        return formataddr(('Logger', 'Logger@gmail.com'))
