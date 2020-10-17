#!/usr/bin/env python3

"""
    __name__: environment.py
    __description__: Script to setup environment related stuffs
    __author__: Abdurrahman Ansari
    __version__: 1.0
    __created__: 2020-04-19
    __updated__: 2020-04-19
"""

import os
import logging


class Env:
    @staticmethod
    def setup_logging() -> logging.Logger:
        """
        Setup logger
        :return: Logger object
        """
        log_dir = os.path.join(os.getcwd(), "logs")
        log_path = os.path.join(log_dir, "pay_slip_analysis.log")

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        logger = logging.getLogger(__name__)

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_path)
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        format_str = "%(asctime)s - [%(filename)s:%(lineno)s - %(funcName)20s()] - %(levelname)s - %(message)s"
        c_format = logging.Formatter(format_str)
        f_format = logging.Formatter(format_str)
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        logger.setLevel(logging.DEBUG)

        return logger
