# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date


class PetBookingLine(models.Model):
    _name = 'pet.booking.line'
    _description = 'Pet Booking Line'
    _order = 'id'

    booking_id = fields.Many2one(
        'pet.booking',
        string="Booking",
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    product_id = fields.Many2one(
        'product.product',
        string="Service",
        required=True,
        domain=[('is_pet_service', '=', True)],
    )
    product_uom_qty = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
        default=0.0,
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_subtotal",
        store=True,
        readonly=True,
    )

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_subtotal(self):
        """Tính thành tiền = Số lượng * Đơn giá"""
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Khi chọn Dịch vụ -> Tự động điền Giá niêm yết vào ô Đơn giá"""
        if self.product_id:
            self.price_unit = self.product_id.list_price or 0.0

    @api.constrains('product_uom_qty')
    def _check_quantity(self):
        """Số lượng dịch vụ phải lớn hơn 0"""
        for line in self:
            if line.product_uom_qty <= 0:
                raise models.ValidationError(
                    _('Số lượng dịch vụ phải lớn hơn 0.')
                )


class PetBooking(models.Model):
    _name = 'pet.booking'
    _description = 'Pet Booking'
    _order = 'booking_date desc, id desc'

    name = fields.Char(
        string="Booking Number",
        required=True,
        readonly=True,
        default='New',
        copy=False,
    )
    booking_date = fields.Date(
        string="Booking Date",
        required=True,
        default=fields.Date.today,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        required=True,
    )
    pet_id = fields.Many2one(
        'pet.pet',
        string="Pet",
        required=True,
        domain="[('owner_id', '=', partner_id)]",
    )
    line_ids = fields.One2many(
        'pet.booking.line',
        'booking_id',
        string="Booking Lines",
    )
    amount_total = fields.Float(
        string="Total",
        compute="_compute_total",
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        default='draft',
    )
    notes = fields.Text(string="Notes")

    @api.depends('line_ids.price_subtotal')
    def _compute_total(self):
        """Tổng phiếu = Tổng các dòng chi tiết"""
        for booking in self:
            booking.amount_total = sum(booking.line_ids.mapped('price_subtotal'))

    @api.constrains('booking_date')
    def _check_booking_date(self):
        """Chặn không cho chọn ngày đặt lịch trong quá khứ"""
        for booking in self:
            if booking.booking_date and booking.booking_date < fields.Date.today():
                raise models.ValidationError(
                    _('Không thể chọn ngày đặt lịch trong quá khứ. Ngày đặt lịch phải từ hôm nay trở đi.')
                )

    @api.model
    def create(self, vals):
        """Tự động tạo mã phiếu"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pet.booking') or _('New')
        return super(PetBooking, self).create(vals)

    def action_confirm(self):
        """Xác nhận phiếu dịch vụ"""
        self.write({'state': 'confirmed'})

    def action_done(self):
        """Hoàn thành phiếu dịch vụ"""
        self.write({'state': 'done'})

    def action_cancel(self):
        """Hủy phiếu dịch vụ"""
        self.write({'state': 'cancelled'})
