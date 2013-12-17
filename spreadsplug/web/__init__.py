import logging
import os

from flask import Flask
from spreads.plugin import HookPlugin, PluginOption

app = Flask('spreadsplug.web', static_url_path='', static_folder='')
import web
import database
logger = logging.getLogger('spreadsplug.web')


class WebCommands(HookPlugin):
    @classmethod
    def add_command_parser(cls, rootparser):
        scanparser = rootparser.add_parser(
            'web-scanner', help="Start the scanning station server")
        scanparser.set_defaults(subcommand=cls.run_scanner_mode)

    @classmethod
    def configuration_template(cls):
        return {
            'project_dir': PluginOption(
                value=u"~/scans",
                docstring="Directory for project folders",
                selectable=False),
            'database': PluginOption(
                value=u"~/.config/spreads/workflows.db",
                docstring="Path to application database file",
                selectable=False),
        }

    @staticmethod
    def run_scanner_mode(config):
        logger.debug("Starting scanning station server")
        app.config['DEBUG'] = True
        # TODO: Setup app configuration from config['web']
        db_path = os.path.expanduser(config['web']['database'].get())
        project_dir = os.path.expanduser(config['web']['project_dir'].get())
        app.config['database'] = db_path
        app.config['base_path'] = project_dir
        app.run()