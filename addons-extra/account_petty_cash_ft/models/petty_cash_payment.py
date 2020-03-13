from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class PettyCashPayment(models.Model):
    _name = 'petty.cash.payment'
    _rec_name = 'holder_id'

    petty_cash_rel = fields.Many2one("petty.cash.book")
    name = fields.Char(string='Name', readonly=True, default='\\')
    date = fields.Date(string='Date', default=datetime.today(), required=True)
    book_id = fields.Many2one('petty.cash.book', string='Book', required=True)
    holder_id = fields.Many2one(related='book_id.petty_cash_holder_id', string='Holder')
    payment_date = fields.Date(string='Payment Date', default=datetime.today(), required=True)
    payment_journal_id = fields.Many2one('account.journal', string='Payment journal ')
    amount = fields.Float(string='Amount')

    # @api.model
    # def create(self, vals):
    #     res = super(PettyCashPayment, self).create(vals)
    #     if res.amount >= res.holder_id.pettycash_limit:
    #         raise ValidationError("Amount should not exceed holders limit set in holders master!")
    #     return res

    @api.constrains('amount')
    def check_amount(self):
        for rec in self:
            if rec.amount >= rec.holder_id.petty_cash_limit:
                raise ValidationError("Amount should not exceed holders limit set in holders master!")
