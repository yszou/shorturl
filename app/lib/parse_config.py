# -*- coding: utf-8 -*-

import os
import logging
import configparser


def parse(file):
    config = configparser.ConfigParser(os.environ, strict=False)
    config.read(file)

    root = config.get('general', 'root')
    static_path = config.get('general', 'static_path')
    template_path = config.get('general', 'template_path')
    log_function = config.get('general', 'log_function')

    config.set('general', 'static_path', os.path.join(root, static_path))
    config.set('general', 'template_path', os.path.join(root, template_path))
    config.set('general', 'log_function', os.path.join(root, log_function))

    for s in config.sections():
        if s.startswith('log:'):
            l = getattr(logging, config.get(s, 'level'))
            config.set(s, 'level', str(l))

    return config


if __name__ == '__main__':
    parse('../config.conf')
