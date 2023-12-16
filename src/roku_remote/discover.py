#!/usr/bin/env python3
"""Send out a M-SEARCH request and listening for responses."""
import asyncio
import logging
import socket
from threading import Thread

import click
import ssdp

logger = logging.getLogger("main")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
@click.command(context_settings=CONTEXT_SETTINGS, options_metavar="<options>")
@click.option("--log-level", help="Log level (default: debug)", type=click.Choice(["debug", "info", "error"]), default="info")
@click.option("--timeout", help="length of time in seconds to keep listening for devices, default 60s", type=click.INT, default=60)
@click.option("--scope", help="defines the scope of the disovery", type=click.STRING, default="ssdp:all")

def main(scope, timeout, log_level):
    """unit test for discovery.
    Discovers all devices, waits for thread to terminate
    """
    if log_level == "debug":
        level = logging.DEBUG
        format='%(asctime)s %(levelname)-8s %(funcName)-32s %(message)s'
    elif log_level == "info":
        level = logging.INFO
    elif log_level == "error":
        level = logging.ERROR

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=level)
    logger.info("discovering ...")
    ssdp_thread = discover(scope, SSDP_ProtocolHandler.default_client_callback, False, timeout)
    ssdp_thread.start()
    ssdp_thread.join()

class SSDP_ProtocolHandler(ssdp.SimpleServiceDiscoveryProtocol):
    """Protocol to handle responses and requests."""

    def default_client_callback(self, header_dict):
        """default callback for unit testing"""
        logger.info(f"discovered: {header_dict}")

    callback = None

    def response_received(self, response: ssdp.SSDPResponse, addr: tuple):
        """Handle an incoming response and call client callback with response headers in dictionary"""
        logger.debug(f"received response: reason: {response.reason} status: {response.status_code}")
        
        header_dict = {}
        # convert the stupid array of name-value tuples into a dictionary
        for header in response.headers:
            header_dict[header[0]] = header[1]
            logger.debug("header: {}".format(header))

        self.callback(header_dict)        
"""
    def request_received(self, request: ssdp.SSDPRequest, addr: tuple):
        #Handle an incoming request.
        logger.debug(
            "received request: {} {} {}".format(
                request.method, request.uri, request.version
            )
        )

        for header in request.headers:
            logger.debug("header: {}".format(header))

        print()
"""

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def discover(search_target, client_callback, force=False, timeout=60):
    """Start the discovery thread"""
    logger.debug(f"discover({search_target}, {client_callback}, {force}, {timeout})")
    ssdp_thread = Thread(target=discover_thread, args=(search_target, client_callback, force, timeout), daemon=True)
    return ssdp_thread

def discover_thread(search_target, client_callback, force, timeout):
    """sends the SSDP request packet on the network and waits for responses"""
    # Start the asyncio loop.
    if SSDP_ProtocolHandler.callback is not None and force == False:
        logger.info("discovery already in progress")
        return
    
    ip_address = get_ip()
    logger.info(f"discovery thread running, ip address is {ip_address}")
    SSDP_ProtocolHandler.callback = client_callback
    loop = asyncio.new_event_loop()
    connect = loop.create_datagram_endpoint(SSDP_ProtocolHandler, local_addr=(ip_address, None), family=socket.AF_INET)
    transport, protocol = loop.run_until_complete(connect)

    logger.debug("sending SSDP request")
    # Send out an M-SEARCH callback = client_callbackrequest, requesting all service types.
    SSDP_PORT = 1900
    search_request = ssdp.SSDPRequest(
        "M-SEARCH",
        headers={
            "HOST": SSDP_ProtocolHandler.MULTICAST_ADDRESS + ":" + str(SSDP_PORT),
            "MAN": '"ssdp:discover"',
            "MX": str(timeout),
            "ST": search_target,
            #"ST": "ssdp:all",
            #"ST": "roku:ecp",
        },
    )   
    sock = transport.get_extra_info('socket')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, timeout)

    search_request.sendto(transport, (SSDP_ProtocolHandler.MULTICAST_ADDRESS, SSDP_PORT))

    # Keep on running for timeout seconds.
    try:
        loop.run_until_complete(asyncio.sleep(timeout))
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()
    SSDP_ProtocolHandler.callback = None
    logger.info("stopping discovery thread")

if __name__ == "__main__":
    main()
    
    
