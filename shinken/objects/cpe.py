#!/usr/bin/python
# -*- coding: utf-8 -*-

from shinken.objects.item import Item, Items
from shinken.property import IntegerProp, BoolProp, StringProp, ListProp, FloatProp

from shinken.log import logger

class Cpe(Item):
    id = 1  # zero is always special in database, so we do not take risk here
    my_type = 'cpe'

    properties = Item.properties.copy()
    properties.update({
        'id': IntegerProp(fill_brok=['full_status']),
        'customerid': IntegerProp(fill_brok=['full_status']),
        'sn': StringProp(fill_brok=['full_status'], default=''),
        'dsn': StringProp(fill_brok=['full_status'], default=''),
        'mac': StringProp(fill_brok=['full_status'], default=''),
        'mtamac': StringProp(fill_brok=['full_status'], default=''),
        'modelid': StringProp(fill_brok=['full_status'], default=''),
        'tech': StringProp(fill_brok=['full_status'], default='docsis'),
        'profileid': IntegerProp(fill_brok=['full_status'], default=None),
        'access': BoolProp(fill_brok=['full_status'], default=True),

        'customer': StringProp(fill_brok=['full_status'], default=None),
        'profile': StringProp(fill_brok=['full_status'], default=None),
        'model': StringProp(fill_brok=['full_status'], default=None),
        'potses': ListProp(default=[], fill_brok=['full_status']),

        'action_url': StringProp(default='', fill_brok=['full_status']),
        'notes_url': StringProp(default=['http://www.elpais.com'], fill_brok=['full_status']),
        'notes': StringProp(default='notes??', fill_brok=['full_status']),
        'notifications_enabled': BoolProp(default=True, fill_brok=['full_status'], retention=True),
        'last_state_change': FloatProp(default=0.0, fill_brok=['full_status', 'check_result'], retention=True),
        'check_command': StringProp(default='_internal_host_up', fill_brok=['full_status']),
    })

    running_properties = Item.running_properties.copy()
    running_properties.update({
        'state': StringProp(default='unknown', fill_brok=['full_status']),
        'output': StringProp(default='en un lugar de la Mancha...', fill_brok=['full_status']),

        'customs': StringProp(default={}, fill_brok=['full_status']),

        'registration_host': StringProp(fill_brok=['full_status'], retention=True),
        'registration_id': IntegerProp(default='?', fill_brok=['full_status'], retention=True),
        'registration_state_id': IntegerProp(default=0, fill_brok=['full_status'], retention=True),
        'registration_state': StringProp(default='PENDING', fill_brok=['full_status'], retention=True),
        'perf_data': StringProp(default='{}', fill_brok=['full_status'], retention=True),

        'latency': FloatProp(default=0, fill_brok=['full_status'], retention=True),

        'comments': StringProp(default=[], fill_brok=['full_status'], retention=True),
        'actions': StringProp(default=[]), # put here checks and notif raised
        'broks': StringProp(default=[]), # and here broks raised
        'last_chk': IntegerProp(default=0, fill_brok=['full_status'], retention=True),
        'downtimes': StringProp(default=[], fill_brok=['full_status'], retention=True),
    })

    def ___init__(self, params={}):
        self.id = None
        self.customerid = None
        self.sn = None
        self.mac = None
        self.mtamac = None
        self.model = None
        self.profileid = None
        self.access = None
        self.potses = []

        self.state = 'PENDING'

        self.action_url = 'http://www.google.es|http://www.google.com'
        self.notes_url = ['http://www.elpais.com']
        self.notes = ['note1', 'note2']
        self.notifications_enabled = True
        self.last_state_change = None
        self.output = 'En un lugar de La Mancha'
        self.last_chk = None
        self.perf_data = 'kara'
        self.downtimes = []

        for key in params:
            if key in ['id', 'customerid', 'sn', 'mac', 'mtamac', 'model', 'profileid', 'access']:
                setattr(self, key, self.properties[key].pythonize(params[key]))

    def __repr__(self):
        return '<cpe#%d/>' % (self.id)

    def __str__(self):
        if self.mac:
            return 'mac%s' % self.mac
        elif self.sn:
            return 'sn%s' % self.sn
        else:
            return 'id%d' % self.id

    def set_registration_info(self, host_name, id, state_id, state, perf_data):
        self.registration_host = host_name
        self.registration_id = id
        self.registration_state_id = state_id
        self.registration_state = state
        self.perf_data = perf_data

        #comment_type = 3 #1:host 2:service?
        #c = Comment(self, persistent, author, comment, comment_type, 4, 0, False, 0)
        #self.add_comment(c)
        self.broks.append(self.get_update_status_brok())

    def get_full_str(self):
        full_name = str(self)
        for pots in self.potses:
            if pots.cli:
                full_name += " " + pots.cli
        return full_name

    get_full_name = get_full_str

    def get_host_tags(self):
        return ['gpon']


class Cpes(Items):
    name_property = 'id'
    inner_class = Cpe

    def linkify(self, customers, cpeprofiles, cpemodels):
        for cpe in self:
            customer = customers.items[cpe.customerid]
            cpe.customer = customer
            customer.add_cpe_link(cpe)

            if cpe.profileid:
                cpeprofile = cpeprofiles.items[cpe.profileid]
                cpe.profile = cpeprofile
                cpeprofile.add_cpe_link(cpe)

            cpemodel = cpemodels.items[cpe.modelid]
            cpe.model = cpemodel
            cpemodel.add_cpe_link(cpe)

    def find_by_id(self, id):
        return self.items.get(int(id), None)

    def find_by_sn(self, sn):
        filter_by_sn = [cpe for cpe in self if cpe.sn and cpe.sn.lower() == sn.lower()]
        if filter_by_sn:
            return filter_by_sn[0]

        filter_by_dsn = [cpe for cpe in self if cpe.dsn and cpe.dsn.lower() == sn.lower()]
        if filter_by_dsn:
            return filter_by_dsn[0]

    def find_by_mac(self, mac):
        filter_by_mac = [cpe for cpe in self if cpe.mac.lower() == mac.lower()]
        if filter_by_mac:
            return filter_by_mac[0]