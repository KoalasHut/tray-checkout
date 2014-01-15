# -*- coding: utf-8 -*-

import os
from datetime import datetime

API_KEY = 'your-key'
API_URL = 'https://api.sandbox.traycheckout.com.br/v2'

# Base Classes

class Base(object):
	def get_attributes__(self):
		return [attribute for attribute in dir(self) if not attribute.startswith("__") and not attribute.endswith("__")]

	def render_items__(self, parent=None, multiple=False):
		attribute_list = []
		template = '&{table}{multiple}[{attribute}]={value}'
		inside_template = '&{parent}[{table}]{multiple}[{attribute}]={value}'

		for attr in self.get_attributes__():
			value = getattr(self, attr)
			# List test
			if isinstance(value, Base):
				attribute_list = attribute_list + value.render_items__(self)
			elif isinstance(value, list):
				for item in value:
					attribute_list = attribute_list + item.render_items__(self, True)
			elif not isinstance(value, list) and value:
				# Mount base dict for template
				kwargs = dict(
					table=self.__table__,
					attribute=attr,
					value=value,
					multiple='[]' if multiple else '')
				# Parent test
				try:
					kwargs['parent'] = parent.__table__
				except Exception, e:
					pass # no parent...
				template = inside_template if parent else template
				attribute_list.append(template.format(**kwargs))

		return attribute_list

	def __repr__(self):
		attributes = self.render_items__()
		return os.linesep.join(attributes)

class Customer(Base):
	def __init__(self, name, cpf, email, **kwargs):
		self.__table__ = 'customer'
		#
		self.name, self.cpf, self.email = name, cpf, email
		self.birth_date = kwargs.get('birth_date', None)

class Contact(Base):
	def __init__(self, type_contact, number_contact):
		self.__table__ = 'contact'
		#
		self.type_contact, self.number_contact = type_contact, number_contact

class Address(Base):
	def __init__(self, type_address, postal_code, street, number, neighborhood, city, state, **kwargs):
		self.__table__ = 'address'
		#
		self.type_address, self.postal_code, self.street, self.number, self.neighborhood, self.city, self.state = \
		type_address, postal_code, street, number, neighborhood, city, state
		self.completion = kwargs.get('completion', None)

class Product(Base):
	def __init__(self, description, quantity, price_unit, **kwargs):
		self.__table__ = 'transaction_product'
		#
		self.description, self.quantity, self.price_unit = description, quantity, price_unit
		self.code = kwargs.get('code', None)
		self.sku_code = kwargs.get('sku_code', None)
		self.extra = kwargs.get('extra', None)

class Transaction(Base):
	def __init__(self, **kwargs):
		self.__table__ = 'transaction'
		#
		self.available_payment_methods = kwargs.get('available_payment_methods', None)
		self.order_number = kwargs.get('order_number', None)
		self.shipping_type = kwargs.get('shipping_type', None)
		self.shipping_price = kwargs.get('shipping_price', None)
		self.price_discount = kwargs.get('price_discount', None)
		self.price_additional = kwargs.get('price_additional', None)
		self.url_notification = kwargs.get('url_notification', None)
		self.free = kwargs.get('free', None)
		self.sub_store = kwargs.get('sub_store', None)

class Payment(Base):
	def __init__(self, payment_method_id, split, **kwargs):
		self.__table__ = 'payment'
		#
		self.payment_method_id, self.split = payment_method_id, split
		self.card_name = kwargs.get('card_name', None)
		self.card_number = kwargs.get('card_number', None)
		self.card_expdate_month = kwargs.get('card_expdate_month', None)
		self.card_expdate_year = kwargs.get('card_expdate_year', None)
		self.card_cvv = kwargs.get('card_cvv', None)

class Affiliates(Base):
	def __init__(self, **kwargs):
		self.__table__ = 'affiliates'
		#
		self.email = kwargs.get('email', None)
		self.percentage = kwargs.get('percentage', None)

# Base Validators

def decimal(text):
    if text[-3] is '.':
        return text
    else:
        raise Exception('"{}"" is not a valid decimal must follow the pattern 0.00 up to 11 chars'.format(text))

def text(text, length):
	if len(text) <= length:
		return text
	else:
		raise Exception('"{}"" supasses the maximum length'.format(text))

def date(text, fmt='%d/%m/%Y'):
	try:
		datetime.strptime(text, fmt)
		return text
	except ValueError, e:
		raise Exception('"{}" is not a valida date, please provide the following format {}'.format(text, fmt))

# Basic Sample

t = Transaction(order_number=666)
p = Payment(1, 5)
c = Contact('pessoal', '1234567890123')

t.payments = [p] # List sample
t.contact = c # Object Sample

print t
