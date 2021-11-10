# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import carb

import omni.ext
from omni.services.core import main

from .services import router


class AssetValidationServiceExtension(omni.ext.IExt):
    """Asset validation extension."""

    def on_startup(self, ext_id) -> None:
        ext_name = ext_id.split("-")[0]
        url_prefix = carb.settings.get_settings_interface().get(f"exts/{ext_name}/url_prefix")

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
        main.deregister_router(router=router)
