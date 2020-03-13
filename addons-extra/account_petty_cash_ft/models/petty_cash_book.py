from odoo import models, fields, api
from datetime import datetime


class PettyCashBook(models.Model):
    _name = 'petty.cash.book'

    petty_cash_holder_id = fields.Many2one('petty.cash.holders', string='Holder', required=True)
    date = fields.Date(string='Date', default=datetime.today(), required=True)
    payment_ids = fields.One2many('petty.cash.payment', 'book_id', string="Payments")
    journal_ids = fields.Many2one('account.journal', string='Journal', required=True)
    expense_ids = fields.One2many('petty.cash.expense', 'book_id', string='Expenses')
    name = fields.Char(string="Book No", required=False, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('valid', 'Valid'), ('in_progress', 'In Progress'),
                              ('closed', 'Closed')],
                             default="draft")

    @api.model
    def create(self, vals):
        sq = self.env['ir.sequence'].next_by_code('petty.cash.book') or 'New'
        vals['name'] = sq
        return super(PettyCashBook, self).create(vals)

    @api.multi
    def action_valid(self):
        for rec in self:
            rec.state = 'valid'

    @api.multi
    def action_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    @api.multi
    def close_action(self):
        for rec in self:
            rec.state = 'closed'
