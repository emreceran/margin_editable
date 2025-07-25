from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # 🔢 Toplu margin alanı
    uniform_margin = fields.Float(
        string="Toplu Margin (%)",
        help="Tüm satırlara uygulanacak margin oranı."
    )

    # 🧮 Karlılık bileşenleri
    product_cost_total = fields.Float(
        string='Ürün Maliyeti',
        compute='_compute_profit_breakdown',
        store=True
    )
    product_profit_total = fields.Float(
        string='Ürün Kârı',
        compute='_compute_profit_breakdown',
        store=True
    )
    service_cost_total = fields.Float(
        string='Servis Maliyeti',
        compute='_compute_profit_breakdown',
        store=True
    )
    service_profit_total = fields.Float(
        string='Servis Kârı',
        compute='_compute_profit_breakdown',
        store=True
    )
    construction_cost_total = fields.Float(
        string='İnşaat Maliyeti',
        compute='_compute_profit_breakdown',
        store=True
    )
    construction_profit_total = fields.Float(
        string='İnşaat Kârı',
        compute='_compute_profit_breakdown',
        store=True
    )

    # 📊 Kategori bazlı toplamlar
    product_total = fields.Float(
        string="Ürün Toplam",
        compute='_compute_profit_totals',
        store=True
    )
    service_total = fields.Float(
        string="Servis Toplam",
        compute='_compute_profit_totals',
        store=True
    )
    construction_total = fields.Float(
        string="İnşaat Toplam",
        compute='_compute_profit_totals',
        store=True
    )
    overall_total = fields.Float(
        string="Genel Karlılık",
        compute='_compute_profit_totals',
        store=True
    )

    # 🧾 Yeni: Genel maliyet ve kar
    total_cost_amount = fields.Float(
        string="Toplam Maliyet",
        compute='_compute_global_profit',
        store=True
    )
    total_profit_amount = fields.Float(
        string="Toplam Kâr",
        compute='_compute_global_profit',
        store=True
    )

    # ⚙️ Margin uygulayıcı
    def apply_uniform_margin(self):
        for order in self:
            for line in order.order_line:
                line.price_unit = line.purchase_price * (1 + order.uniform_margin / 100)
                line.margin_yeni = order.uniform_margin

    # 🔍 Kâr/Maliyet hesaplayıcı
    @api.depends('order_line.product_id', 'order_line.product_uom_qty', 'order_line.purchase_price', 'order_line.price_subtotal')
    def _compute_profit_breakdown(self):
        for order in self:
            prod_cost = prod_rev = serv_cost = serv_rev = const_cost = const_rev = 0.0
            for line in order.order_line:
                cost = line.purchase_price * line.product_uom_qty
                revenue = line.price_subtotal
                category = line.product_id.categ_id

                if category and category.name == "İŞ MAKİNALARI VE İNŞAAT ELEMANLARI":
                    const_cost += cost
                    const_rev += revenue
                elif line.product_id.type == 'service':
                    serv_cost += cost
                    serv_rev += revenue
                else:
                    prod_cost += cost
                    prod_rev += revenue

            order.product_cost_total = prod_cost
            order.product_profit_total = prod_rev - prod_cost
            order.service_cost_total = serv_cost
            order.service_profit_total = serv_rev - serv_cost
            order.construction_cost_total = const_cost
            order.construction_profit_total = const_rev - const_cost

    # 📊 Toplam alan hesaplayıcı
    @api.depends(
        'product_cost_total', 'product_profit_total',
        'service_cost_total', 'service_profit_total',
        'construction_cost_total', 'construction_profit_total'
    )
    def _compute_profit_totals(self):
        for order in self:
            order.product_total = (order.product_cost_total or 0.0) + (order.product_profit_total or 0.0)
            order.service_total = (order.service_cost_total or 0.0) + (order.service_profit_total or 0.0)
            order.construction_total = (order.construction_cost_total or 0.0) + (order.construction_profit_total or 0.0)
            order.overall_total = order.product_total + order.service_total + order.construction_total

    # 🧾 Genel maliyet ve kar hesaplayıcı
    @api.depends('order_line.purchase_price', 'order_line.product_uom_qty', 'order_line.price_subtotal')
    def _compute_global_profit(self):
        for order in self:
            total_cost = 0.0
            total_profit = 0.0
            for line in order.order_line:
                cost = line.purchase_price * line.product_uom_qty
                revenue = line.price_subtotal
                total_cost += cost
                total_profit += revenue - cost
            order.total_cost_amount = total_cost
            order.total_profit_amount = total_profit
