# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Margin Editable',
    'summary': 'Satış siparişi satırındaki marj (%) alanını manuel düzenlenebilir yapar.',
    'description': """
        Bu modül, satış siparişi satırındaki standart kar marjı (%) alanını (margin)
        elle düzenlenebilir hale getirir ve girilen marj yüzdesine göre satış fiyatını (price_unit) ayarlar.
    """,
    'author': 'Your Name/Company Name', # Kendi adınızı veya şirket adınızı yazın
    'website': 'http://www.yourwebsite.com', # Kendi web sitenizi yazın
    'category': 'Sales',
    'version': '1.0',
    'depends': ['sale_management', 'product', 'sale_margin'], # sale_margin'e bağımlı olmalı
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}