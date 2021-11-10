# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import argparse
import os

import packmanapi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create folder link to Kit App installed from Omniverse Launcher.")
    parser.add_argument(
        "path",
        help="Path to Kit App installed from Omniverse Launcher, e.g.: 'C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4'",
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Provided path doesn't exist: \"{args.path}\"")
    else:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        packmanapi.link(f"{SCRIPT_ROOT}/../../app", args.path)
