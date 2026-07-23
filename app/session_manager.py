"""
==========================================
MOS Practice V15
Session Manager
==========================================
"""

import json
import os


class SessionManager:

    def __init__(self, logger):

        self.logger = logger

        self.session_file = "session.json"

    def save(self, data):

        with open(
            self.session_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )
            
        self.logger.info(
            f"Session saved: "
            f"Project={data['project']} "
            f"Task={data['task']}"
        )
        

    def load(self):

        if not os.path.exists(self.session_file):
            
            self.logger.warning(
                "Session file not found. Using default session."
            )
            
            return None

        with open(
            self.session_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


        

        
        
