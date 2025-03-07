# IMPORTATION STANDARD
import logging
from typing import Dict, Optional

# IMPORTATION THIRD PARTY
import requests

# IMPORTATION INTERNAL
from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
)


class ActionCreateFavouriteList(AbstractAction):
    @classmethod
    def favorite_list_to_api(cls, name: str) -> Dict[str, str]:
        return {"name": name}

    @classmethod
    def api_to_favorite_list_id(cls, response_dict: Dict[str, int]) -> int:
        return response_dict["data"]

    @classmethod
    def create_favourite_list(
        cls,
        name: str,
        session_id: str,
        credentials: Credentials,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Optional[int]:
        """Create a favourite list.
        Args:
            name (str):
                New name of the favorite list.
            session_id (str):
                API's session id.
            credentials (Credentials):
                Credentials containing the parameter "int_account".
            raw (bool, optional):
                Whether are not we want the raw API response.
                Defaults to False.
            session (requests.Session, optional):
                This object will be generated if None.
                Defaults to None.
            logger (logging.Logger, optional):
                This object will be generated if None.
                Defaults to None.
        Returns:
            Favourites: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.PRODUCT_FAVOURITES_LISTS

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        favorite_list_dict = cls.favorite_list_to_api(name=name)

        request = requests.Request(
            method="POST",
            url=url,
            params=params,
            json=favorite_list_dict,
        )
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()
            response_dict = response_raw.json()
            favorite_list_id = cls.api_to_favorite_list_id(response_dict=response_dict)
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return favorite_list_id

    def call(
        self,
        name: str,
    ) -> Optional[int]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.create_favourite_list(
            name=name,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
