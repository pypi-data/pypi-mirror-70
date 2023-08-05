import copy

__post_permission_request = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'private_info': {
                    'type': 'string',
                    'minLength': 1
                },
                'transaction': {
                    'type': 'object',
                    'properties': {
                        'originator_vasp_code': {
                            'type': 'string',
                            'minLength': 1
                        },
                        'originator_addrs': {
                            'type': 'array',
                            'minItems': 1,
                            'items': [
                                {
                                    'type': 'string',
                                    'minLength': 1
                                }
                            ]
                        },
                        'originator_addrs_extra': {
                            'type': 'object',
                            'minProperties': 1
                        },
                        'beneficiary_vasp_code': {
                            'type': 'string',
                            'minLength': 1
                        },
                        'beneficiary_addrs': {
                            'type': 'array',
                            'minItems': 1,
                            'items': [
                                {
                                    'type': 'string',
                                    'minLength': 1
                                }
                            ]
                        },
                        'beneficiary_addrs_extra': {
                            'type': 'object',
                            'minProperties': 1
                        },
                        'transaction_currency': {
                            'type': 'string',
                            'minLength': 1
                        },
                        'amount': {
                            'type': 'number',
                            'exclusiveMinimum': 0
                        }
                    },
                    'required': [
                        'originator_vasp_code',
                        'originator_addrs',
                        'beneficiary_vasp_code',
                        'beneficiary_addrs',
                        'transaction_currency',
                        'amount'
                    ],
                    'additionalProperties': False
                },
                'data_dt': {
                    'format': 'date-time'
                },
                'signature': {
                    'type': 'string',
                    'minLength': 128,
                    'maxLength': 128,
                    'pattern': '^[0123456789A-Fa-f]+$'
                },
                'expire_date': {
                    'type': 'number',
                    'minimum': 0
                }
            },
            'required': [
                'private_info',
                'transaction',
                'data_dt',
                'signature'
            ],
            'additionalProperties': False
        },
        'callback': {
            'type': 'object',
            'properties': {
                'callback_url': {
                    'type': 'string',
                    'format': 'uri'
                },
                'signature': {
                    'type': 'string',
                    'minLength': 128,
                    'maxLength': 128,
                    'pattern': '^[0123456789A-Fa-f]+$'
                }
            },
            'required': [
                'callback_url',
                'signature'
            ],
            'additionalProperties': False
        }
    },
    'required': [
        'data',
        'callback'
    ],
    'additionalProperties': False
}


def get_post_permission_request_schema() -> dict:
    clone_schema = copy.deepcopy(__post_permission_request)
    return clone_schema
