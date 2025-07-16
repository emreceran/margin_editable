# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # 'margin' alanı yerine yeni bir alan tanımlıyoruz: margin_yeni
    margin_yeni = fields.Float(
        string='Kar (%)',  # Alanın görünen adı
        digits='Product Price',
        help="Bu satış satırı için manuel olarak girilebilen kar marjı yüzdesi. Satış fiyatını etkiler.",
        store=True,  # Veritabanında saklanır
        default=0.0,  # Varsayılan değeri sıfır
    )

    # Yeni marj yüzdesi (margin_yeni) değiştiğinde price_unit'i güncelleyen onchange metodu
    @api.onchange('margin_yeni', 'purchase_price')
    def _onchange_margin_yeni_update_price_unit(self):
        # Yalnızca ürün, purchase_price ve margin_yeni geçerli değerlere sahipse hesaplama yap
        if self.product_id and self.purchase_price is not None and self.purchase_price > 0 and self.margin_yeni is not None:
            if self.margin_yeni >= 100.0:
                raise UserError(
                    _("Kar marjı %100 veya daha fazla olamaz çünkü bu durumda satış fiyatı sonsuz olur veya kar elde edilemez."))

            margin_factor = (100.0 - self.margin_yeni) / 100.0
            if margin_factor == 0:  # Eğer marj %100 ise sıfıra bölme hatasını önle
                raise UserError(_("Kar marjı %100 olamaz. Lütfen geçerli bir yüzde girin."))

            # price_unit'i (satış fiyatı) hesapla: purchase_price / (1 - margin_yeni / 100)
            self.price_unit = self.purchase_price / margin_factor

        elif self.product_id and self.purchase_price is not None:
            # Eğer margin_yeni sıfırlanırsa veya ürün yoksa, price_unit'i purchase_price'a eşitle (marj sıfır)
            self.price_unit = self.purchase_price
        else:
            self.price_unit = 0.0