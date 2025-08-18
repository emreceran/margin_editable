# -*- coding: utf-8 -*-
# from odoo import http


# class MarginEditable(http.Controller):
#     @http.route('/margin_editable/margin_editable', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/margin_editable/margin_editable/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('margin_editable.listing', {
#             'root': '/margin_editable/margin_editable',
#             'objects': http.request.env['margin_editable.margin_editable'].search([]),
#         })

#     @http.route('/margin_editable/margin_editable/objects/<model("margin_editable.margin_editable"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('margin_editable.object', {
#             'object': obj
#         })

