#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils import get_uid, compress, decompress, pack, unpack
from .errors import PutError, GetError, CommitError
import pickle
import requests
import json
import time


class Message:
    def __init__(self, stream, partition, index, value, timestamp, **kwargs):
        self.stream = stream
        self.partition = partition
        self.index = index
        self.value = value
        self.timestamp = timestamp


class Sender:
    def __init__(self, endpoint: str, stream: str):
        self.endpoint = endpoint
        self.stream = stream
        self.session = requests.Session()

    def put(self, value, stream: str = None, key: str = None) -> dict:
        stream = stream if stream else self.stream

        data = {
            'method': 'put_message',
            'params': {
                'value': pickle.dumps(value),
                'stream': stream,
            }
        }

        if key is not None:
            data['params']['key'] = key

        response = self.session.post(self.endpoint, data=compress(pack(data))).json()
        if response['status'] != 'ok':
            raise PutError


class Receiver:
    def __init__(self, endpoint, stream=None, receiver_group=None, instance=None):
        self.endpoint = endpoint
        self.stream = stream
        self.receiver_group = receiver_group
        if instance is None:
            instance = get_uid()
        self.instance = instance
        self.session = requests.Session()

    def get(self, stream: str = None, receiver_group: str = None, instance: str = None) -> Message:
        while True:
            instance = instance if instance else self.instance
            stream = stream if stream else self.stream
            receiver_group = receiver_group if receiver_group else self.receiver_group

            if receiver_group is None:
                raise ValueError('stream was not provided')

            if stream is None:
                raise ValueError('stream was not provided')

            data = json.dumps({
                'method': 'get_message',
                'params': {
                    'stream': stream,
                    'receiver': receiver_group,
                    'instance': instance
                }
            })

            try:
                response = self.session.post(self.endpoint, data=data)
                message = unpack(decompress(response.content))
            except Exception:
                yield from self.get(stream, receiver_group, instance)
                return

            if message['status'] == 'end_of_stream':
                time.sleep(0.5)
                continue

            elif message['status'] != 'ok':
                raise GetError

            yield Message(**message)

    def commit(self, message, receiver_group: str = None):
        receiver_group = receiver_group if receiver_group else self.receiver_group

        data = json.dumps({
            'method': 'commit_message',
            'params': {
                'stream': message.stream,
                'partition': message.partition,
                'index': message.index,
                'receiver': receiver_group,
            }
        })

        response = self.session.post(self.endpoint, data=data).json()
        if response['status'] != 'ok':
            raise CommitError