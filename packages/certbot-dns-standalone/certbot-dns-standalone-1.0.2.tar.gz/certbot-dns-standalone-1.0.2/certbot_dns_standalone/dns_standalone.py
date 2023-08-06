"""Standalone DNS Authenticator."""
import logging

import copy

from dnslib import RR
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)
dnsLogger = DNSLogger("truncated,error",False)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """Standalone DNS Authenticator

    This Authenticator uses a standalone DNS server to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using an integrated DNS server')

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.resolver = None
        self.udp_server = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=0)
        add('address', help='IP address to bind to.', default='0.0.0.0')
        add('port', help='Port to bind to.', default='53')

    def _setup_credentials(self):
        return

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin uses a standalone DNS server to respond to a dns-01 challenge.'

    def _perform(self, domain, validation_name, validation):
        if self.resolver is None:
            self.resolver = _AcmeResolver()

        self.resolver.addToken(validation)

        if self.udp_server is None:
            try:
                self.udp_server = DNSServer(self.resolver, port=int(self.conf('port')), address=self.conf('address'),
                                            logger=dnsLogger)
                self.udp_server.start_thread()
            except Exception as e:
                raise errors.PluginError('Error starting DNS server: {0}'.format(e))

    def _cleanup(self, domain, validation_name, validation):
        if self.udp_server:
            self.udp_server.stop()


class _AcmeResolver(BaseResolver):
    def __init__(self):
        self.tokens = []

    def addToken(self,validation):
        self.tokens.append(validation)

    def resolve(self,request,handler):
        reply = request.reply()
        qname = request.q.qname

        if request.q.qtype == 16:
            records = ""
            for r in self.tokens:
                records += ". 60 TXT %s\n" % r

            resp = RR.fromZone(records)
        else:
            resp = RR.fromZone(". 60 A 127.0.0.1") # for dig

        if request.q.qtype == 1 or request.q.qtype == 16:
            for rr in resp:
                a = copy.copy(rr)
                a.rname = qname
                reply.add_answer(a)

        return reply
