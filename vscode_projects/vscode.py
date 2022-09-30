from cmath import log
from logging import Logger
import logging
import os
import json
import glob
import datetime
import sqlite3;
from memoization import cached
from typing import List


class Client(object):
    """ Client to interact with VS Code API"""

    @cached(ttl=60)
    def get_projects(self, preferences: dict):
        """ Returns projects """


        workspace_projects = []

        names_index = []


        workspace_projects = self.get_projects_from_workspaces(
            preferences, names_index)

        all_projects = workspace_projects
        return all_projects

    def get_projects_from_workspaces(self, preferences: dict,
                                     exclude_list: List[str]):
        """ Reads VS Code recent workspaces """
        abs_path = os.path.expanduser(preferences['config_path'])
        state_db_path = glob.glob(abs_path +
                              "/User/globalStorage/state.vscdb");

        con = sqlite3.connect(state_db_path[0])

        cur = con.cursor()

        cur.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList'")

        rows = cur.fetchall()

        logger = logging.getLogger(__name__)

        logger.debug("Rows: %s", rows[0])

        openedPathList: dict = json.loads(rows[0][0])

        entries = openedPathList['entries']


        recent_workspaces = []

        for entry in entries:

            workspace = {}

            # logger.debug("Entry: %s", entry)

            if 'folderUri' not in entry: continue

            logger.debug("Entry: %s", entry)


            workspace['path'] = entry['folderUri']


            if 'label' in entry:
                workspace['name'] = entry['label'].split('/')[-1]
            else:
                workspace['name'] = entry['folderUri'].split('/')[-1]


            workspace['type'] = 'workspace'

            recent_workspaces.append(workspace)

        return recent_workspaces
