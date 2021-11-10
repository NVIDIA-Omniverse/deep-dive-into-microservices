# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import asyncio
from typing import List, Optional

from pxr import UsdGeom
from pydantic import BaseModel, Field

import carb
from omni.services.core import routers
import omni.usd


router = routers.ServiceAPIRouter()


class ValidationRequestModel(BaseModel):
    """Model describing the request to validate a given USD stage."""

    scene_path: str = Field(
        ...,
        title="USD scene path",
        description="Full path to the USD scene to validate, hosted on a location accessible to the Agent.",
    )
    expected_camera_count: int = Field(
        ...,
        title="Expected number of cameras",
        description="Expected number of cameras to find in the scene.",
    )


class ValidationResponsetModel(BaseModel):
    """Model describing the response to the request to validate a given USD stage."""

    success: bool = Field(
        ...,
        title="Success",
        description="Flag indicating if the validation was successful.",
    )
    actual_camera_count: int = Field(
        ...,
        title="Number of cameras found",
        description="Actual number of cameras found in the scene.",
    )


async def load_usd_stage(usd_file: str, stage_load_timeout: Optional[float] = None) -> bool:
    """
    Load the given USD stage into the Kit runtime.

    Args:
        usd_file (str): Location of the stage to open.
        stage_load_timeout (Optional[float]): Maximum duration for which to wait before considering a loading timeout.

    Returns:
        bool: A flag indicating whether or not the given USD stage was successfully loaded.
    """
    success, error = await omni.usd.get_context().open_stage_async(usd_file)
    if not success:
        carb.log_error(f"Unable to open \"{usd_file}\": {str(error)}")
        raise Exception(f"Unable to open \"{usd_file}\".")

    carb.log_info("Stage opened. Waiting for \"ASSETS_LOADED\" event.")

    usd_context = omni.usd.get_context()
    if usd_context.get_stage_state() != omni.usd.StageState.OPENED:
        while True:
            try:
                event, _ = await asyncio.wait_for(usd_context.next_stage_event_async(), timeout=stage_load_timeout)
                if event == int(omni.usd.StageEventType.ASSETS_LOADED):
                    carb.log_info(f"Assets for \"{usd_file}\" loaded")
                    return True
            except asyncio.TimeoutError:
                _, files_loaded, total_files = usd_context.get_stage_loading_status()
                if files_loaded == total_files:
                    carb.log_warn("Timed out waiting for \"ASSETS_LOADED\" event but all files seem to have loaded.")
                    return False

                raise Exception(f"Timed out waiting for \"ASSETS_LOADED\" event for \"{usd_file}\". Aborting.")


def get_all_stage_cameras() -> List[UsdGeom.Camera]:
    """
    Return the list of all USD cameras found the current USD stage.

    Args:
        None

    Returns:
        List[UsdGeom.Camera]: The list of all USD cameras found in the current USD stage.
    """
    cameras: List[UsdGeom.Camera] = []
    stage = omni.usd.get_context().get_stage()

    for prim in stage.TraverseAll():
        if prim.IsA(UsdGeom.Camera):
            cameras.append(UsdGeom.Camera(prim))

    return cameras


@router.post(
    path="/validate",
    summary="Validate assets for conformity",
    description="Validate that the USD Stage at the given location conforms to pre-determined validation rules.",
    response_model=ValidationResponsetModel,
)
async def run(req: ValidationRequestModel) -> ValidationResponsetModel:
    # Load the USD stage:
    await load_usd_stage(usd_file=req.scene_path)

    # Perform the validation.
    #
    # NOTE: For demonstration purposes, we are only considering the number of cameras present in the given USD scene to
    # demonstrate integration with tools and workflows.
    stage_cameras = get_all_stage_cameras()
    camera_count = len(stage_cameras)
    validation_success = camera_count == req.expected_camera_count

    # Return the validation results:
    return ValidationResponsetModel(
        success=validation_success,
        actual_camera_count=camera_count,
    )
