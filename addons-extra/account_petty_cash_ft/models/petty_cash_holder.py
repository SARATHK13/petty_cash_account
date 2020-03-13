from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritAccountJournal(models.Model):
    _inherit = 'account.journal'

    is_petty_cash = fields.Boolean(string='Petty Cash')


class PettyCashHolder(models.Model):

    _name = 'petty.cash.holders'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    name = fields.Char(string='Name', related='partner_id.name', readonly=True)
    account_id = fields.Many2one('account.account', string='PettyCash Account', required=True)
    petty_cash_limit = fields.Float(string='PettyCash Limit', required=True)

    @api.model
    def create(self, vals):
        res = super(PettyCashHolder, self).create(vals)
        if res.petty_cash_limit <= 0:
            raise ValidationError("PettyCash Limit Should be greater than zero!")
        return res


class PettyCashExpense(models.Model):
    _name = 'petty.cash.expense'

    book_id = fields.Many2one('petty.cash.book', string='Book', required=True)
