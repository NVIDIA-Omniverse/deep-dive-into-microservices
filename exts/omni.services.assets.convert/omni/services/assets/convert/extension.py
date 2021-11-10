# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import asyncio

import carb

import omni.ext
from omni.services.core import main
from omni.services.facilities.database.manager import DatabaseManagerFacility

from .services import router


class AssetConversionServiceExtension(omni.ext.IExt):
    """Asset conversion extension."""

    def on_startup(self, ext_id) -> None:
        ext_name = ext_id.split("-")[0]
        url_prefix = carb.settings.get_settings_interface().get(f"exts/{ext_name}/url_prefix")

        # Setup the database facility:
        self._database_facility = DatabaseManagerFacility(ext_name=ext_name)
        self._db_ready = asyncio.ensure_future(self._initialize_db())

        # Register the database facility with the router, so it can be used by service endpoints:
        router.register_facility("db_manager", self._database_facility)

        main.register_router(router=router, prefix=url_prefix, tags=["Assets"])
        main.get_app().title = "Omniverse Farm"
        main.get_app().description = "A microservice-based framework for distributed task execution."

        tags_metadata = {
            "name": "Assets",
            "description": "Manage assets submitted to the Queue."
        }
        if not main.get_app().openapi_tags:
            main.get_app().openapi_tags = []
        main.get_app().openapi_tags.append(tags_metadata)

    def on_shutdown(self) -> None:
        if self._db_ready:
            self._db_ready.cancel()
            self._db_ready = None
        main.deregister_router(router=router)

    async def _initialize_db(self) -> None:
        """Initialize the database to be used to store asset conversion results."""
        async with self._database_facility.get("asset-conversions") as db:
            table_columns = [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "source_asset VARCHAR(256) NOT NULL",
                "destination_asset VARCHAR(256) NOT NULL",
                "success BOOLEAN NOT NULL",
            ]
            await db.execute(query=f"CREATE TABLE IF NOT EXISTS AssetConversions ({', '.join(table_columns)});")
