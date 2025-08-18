# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_yeni = fields.Float(
        string='Yeni Margin (%)',
        digits='Product Price',
        help="Bu satış satırı için manuel olarak girilebilen kar marjı yüzdesi. Maliyet üzerinden hesaplanır ve satış fiyatını etkiler.",
        store=True,
        default=0.0,
    )

    @api.onchange('margin_yeni', 'purchase_price')
    def _onchange_margin_yeni_update_price_unit(self):

        # --- DÜZELTİLMİŞ KISIM ---
        # Kategori adını küçük harfe çevirerek büyük/küçük harf duyarlılığı kaldırıldı.
        if self.product_id and self.product_id.categ_id.id == 61:
            print("asasa")
            return
        # --- DÜZELTME SONU ---

        if self.product_id and self.purchase_price is not None and self.margin_yeni is not None:
            calculated_price_unit = self.purchase_price * (1 + self.margin_yeni / 100.0)

            if calculated_price_unit < 0:
                raise UserError(_("Hesaplanan satış fiyatı negatif olamaz. Lütfen geçerli bir kar marjı girin."))

            self.price_unit = calculated_price_unit

        elif self.product_id and self.purchase_price is not None:
            self.price_unit = self.purchase_price
        else:
            self.price_unit = 0.0