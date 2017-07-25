#!/usr/bin/env python

import io
import socket
import argparse

import avro.io
import avro.datafile
import pkg_resources

from mdcs.tcp.schema import REQUEST_SCHEMA, RESPONSE_SCHEMA


def main():
    """
    Run the bridge node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="node hostname or IP address")
    parser.add_argument('--http-port', type=int, default=5510, help="HTTP API port")
    parser.add_argument('--tcp-port', type=int, default=5511, help="TCP API port")

    args = parser.parse_args()

    # TODO: connect to the server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((args.host, args.tcp_port))

    # TODO: create the request
    request = {'command': {'device': 'hue', 'attribute': 'serial'}}

    # TODO: serialize the request
    request_buffer = io.BytesIO()
    writer = avro.datafile.DataFileWriter(request_buffer, avro.io.DatumWriter(), REQUEST_SCHEMA)
    writer.append(request)
    writer.flush()

    # TODO: send the request
    request_buffer.seek(0)
    request_data = request_buffer.read()
    tcp_socket.send(request_data)

    # TODO: read the response
    response_data = tcp_socket.recv(10240)
    response_buffer = io.BytesIO(response_data)
    reader = avro.datafile.DataFileReader(response_buffer, avro.io.DatumReader())

    # TODO: process the response
    for response in reader:
        result = response['result']
        if 'message' in result:
            print("error: {0}".format(result))

        else:
            when = result['when']
            data = result['value']

            data_reader = avro.datafile.DataFileReader(io.BytesIO(data), avro.io.DatumReader())
            for value in data_reader:
                print("value: {0} @ {1}".format(value, when))

            data_reader.close()

    # TODO: close the reader
    reader.close()
