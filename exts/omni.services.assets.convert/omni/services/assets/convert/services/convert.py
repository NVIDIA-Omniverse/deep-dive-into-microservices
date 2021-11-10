# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from typing import Dict

from pydantic import BaseModel, Field

from omni.services.client import AsyncClient
from omni.services.core import routers
import omni.usd


router = routers.ServiceAPIRouter()


class ConversionRequestModel(BaseModel):
    """Model describing the request to convert a given asset to a different format."""

    import_path: str = Field(
        ...,
        title="Path of the source asset to be converted",
        description="Location where the asset to convert can be located by an Agent.",
    )
    output_path: str = Field(
        ...,
        title="Output path where to store the converted asset",
        description="Location where to place the converted asset.",
    )
    converter_settings: Dict = Field(
        {},
        title="Converter settings",
        description="Settings to provide to the Kit Asset Converter extension in order to perform the conversion.",
    )


class ConversionResponseModel(BaseModel):
    """Model describing the response to the request to convert a given USD asset."""

    status: str = Field(
        ...,
        title="Conversion status",
        description="Status of the conversion of the given asset.",
    )


@router.post(
    path="/convert",
    summary="Convert assets to a different format",
    description="Convert the given asset into a different format.",
    response_model=ConversionResponseModel,
)
@router.post("/convert")
async def run(
    req: ConversionRequestModel,
    db_manager=router.get_facility("db_manager"),
) -> ConversionResponseModel:
    # Convert the given asset:
    task = omni.kit.asset_converter.get_instance().create_converter_task(
        import_path=req.import_path,
        output_path=req.output_path,
        progress_callback=lambda current, total: print(f"Conversion progress: {current/total*100.0}%"),
        asset_converter_context=req.converter_settings,)
    success = await task.wait_until_finished()
    if not success:
        detailed_status_code = task.get_status()
        detailed_status_error_string = task.get_detailed_error()
        raise Exception(f"Failed to convert \"{req.import_path}\". Error: {detailed_status_code}, {detailed_status_error_string}")

    # Execute the validation service exposed by the "omni.service.assets.validate" extension:
    client = AsyncClient("local://")
    validation_result = await client.assets.validate(
        scene_path=req.import_path,
        expected_camera_count=5,
    )

    # Record the result of the validation in the database:
    query = """
        INSERT INTO AssetConversions (source_asset, destination_asset, success)
        VALUES (:source_asset, :destination_asset, :success)
    """
    values = {
        "source_asset": req.import_path,
        "destination_asset": req.output_path,
        "success": 1 if validation_result["success"] else 0,
    }
    async with db_manager.get("asset-conversions") as db:
        await db.execute(query=query, values=values)

    return ConversionResponseModel(status="finished")
