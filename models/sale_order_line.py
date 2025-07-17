# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_yeni = fields.Float(
        string='Yeni Margin (%)',  # Alanın kullanıcı arayüzünde görünecek adı
        digits='Product Price',  # Sayısal hassasiyet ayarı
        help="Bu satış satırı için manuel olarak girilebilen kar marjı yüzdesi. Maliyet üzerinden hesaplanır ve satış fiyatını etkiler.",
        store=True,  # Değeri veritabanında sakla
        default=0.0,  # Varsayılan değeri sıfır
    )

    # Yeni marj yüzdesi (margin_yeni) değiştiğinde veya purchase_price değiştiğinde price_unit'i güncelleyen onchange metodu
    @api.onchange('margin_yeni', 'purchase_price')
    def _onchange_margin_yeni_update_price_unit(self):
        # Yalnızca ürün seçili ise ve gerekli fiyat bilgileri mevcutsa işlem yap.
        # Bu durumda, purchase_price'ın ve margin_yeni'nin None olmaması yeterli.
        # purchase_price'ın 0'dan büyük olması, sıfır maliyetli ürünler için de geçerli olabilir,
        # ama yüzde hesaplaması için pozitif olması genellikle beklenir.
        if self.product_id and self.purchase_price is not None and self.margin_yeni is not None:
            # Yeni hesaplama mantığı: price_unit = purchase_price + (purchase_price * margin_yeni / 100)
            # Veya: price_unit = purchase_price * (1 + margin_yeni / 100)

            # Eğer kar marjı negatif olursa (indirim gibi), satış fiyatı maliyetin altına düşer.
            # Buna izin verip vermeyeceğiniz iş gereksiniminize bağlıdır.
            # Şu anki varsayım: negatif kar marjına izin veriyoruz, ama satış fiyatı negatif olamaz.

            calculated_price_unit = self.purchase_price * (1 + self.margin_yeni / 100.0)

            if calculated_price_unit < 0:
                raise UserError(_("Hesaplanan satış fiyatı negatif olamaz. Lütfen geçerli bir kar marjı girin."))

            self.price_unit = calculated_price_unit

        elif self.product_id and self.purchase_price is not None:
            # Eğer ürün ve satın alma fiyatı varsa ancak margin_yeni sıfır ise veya silinmişse,
            # price_unit'i doğrudan purchase_price'a eşitle (yani marj sıfır kabul edilir).
            self.price_unit = self.purchase_price
        else:
            # Ürün veya purchase_price yoksa, price_unit'i sıfır yap.
            self.price_unit = 0.0