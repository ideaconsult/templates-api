import json
import os
import shutil
import time
import traceback
import uuid
from pathlib import Path

import nexusformat.nexus.tree as nx
import pandas as pd
import requests
from fastapi import HTTPException
from pyambit.datamodel import Substances
from pyambit.nexus_writer import to_nexus
from pynanomapper.datamodel.templates.template_parser import TemplateDesignerParser

from tplapi.config.app_config import initialize_dirs

config, UPLOAD_DIR, NEXUS_DIR, TEMPLATE_DIR = initialize_dirs()


def parse_template_designer_files(task, base_url, excel_path):
    # Convert Excel to NeXus using pynanomapper
    try:
        # Parse Excel file
        parser = TemplateDesignerParser(excel_path)
        # Convert to Substances with study data
        substances = parser.to_substances()
        convert_to_nexus(substances, task, base_url, dataset_uuid=str(uuid.uuid4()))
        task.status = "Completed"
        task.result = f"{base_url}dataset/{task.result_uuid}?format=nxs"
    except Exception as err:
        task.result = (f"{base_url}task/{task.id}?format=json",)
        task.result_uuid = None
        task.status = "Error"
        task.error = str(err)
        task.errorCause = traceback.format_exc()
        task.completed = int(time.time() * 1000)


async def process(
    task, dataset_type, file_path, jsonconfig_path, expandconfig_path, base_url
):
    try:
        # Save uploaded file to a temporary location
        file_extension = Path(file_path).suffix
        ext = file_extension.replace(".", "")
        task.result = (f"{base_url}task/{task.id}?format={ext}",)

        dataset_type = "template_wizard"
        if file_extension.lower() == ".xlsx" or file_extension.lower() == ".xls":
            try:
                xls = pd.ExcelFile(file_path)
                if "TemplateDesigner" in xls.sheet_names:
                    parse_template_designer_files(task, base_url, excel_path=file_path)
                else:  # Template Wizard files need external config
                    parse_template_wizard_files(
                        task, base_url, file_path, jsonconfig_path, expandconfig_path
                    )
                task.status = "Completed"
            except HTTPException:
                task.error = "error parsing file"
        else:
            task.error = f"Unsupported file {file_path} of type {dataset_type}"
            task.status = "Error"
        task.completed = int(time.time() * 1000)
    except Exception as err:
        task.error = str(err)
        task.status = "Error"
        task.completed = int(time.time() * 1000)


def convert_to_nexus(substances: Substances, task, base_url, dataset_uuid):
    try:

        nxroot = substances.to_nexus(hierarchy=False)
        nexus_file_path = os.path.join(NEXUS_DIR, f"{dataset_uuid}.nxs")
        nxroot.save(nexus_file_path, mode="w")
        task.status = "Completed"
        task.result = f"{base_url}h5grove/{dataset_uuid}?format=nxs"
        task.result_uuid = dataset_uuid
        task.completed = int(time.time() * 1000)
    except Exception as perr:
        task.result_uuid = None
        task.result = (f"{base_url}dataset/{dataset_uuid}?format=json",)
        task.status = "Error"
        task.error = f"Error converting to hdf5 {perr}"
        task.errorCause = traceback.format_exc()
        task.completed = int(time.time() * 1000)


def parse_template_wizard_files(
    task, base_url, file_path, jsonconfig_path, expandconfig_path=None
):
    if jsonconfig_path is None:
        task.status = "Error"
        task.error = "Missing jsonconfig"
        task.result_uuid = None
    else:
        parsed_file_path = os.path.join(UPLOAD_DIR, f"{task.id}.json")
        try:
            parsed_json = nmparser(file_path, jsonconfig_path)
            with open(parsed_file_path, "w") as json_file:
                json.dump(parsed_json, json_file)
            substances = Substances(**parsed_json)
            convert_to_nexus(substances, task, base_url)
        except Exception as perr:
            task.result = (f"{base_url}dataset/{task.id}?format=json",)
            task.result_uuid = None
            task.status = "Error"
            task.error = f"Error parsing template wizard files {perr}"
            task.errorCause = traceback.format_exc()
    task.completed = int(time.time() * 1000)


def nmparser(xfile, jsonconfig, expandfile=None):
    with open(xfile, "rb") as fin:
        with open(jsonconfig, "rb") as jin:
            form = {"files[]": fin, "jsonconfig": jin, "expandfile": expandfile}
            try:
                response = requests.post(config.nmparse_url, files=form, timeout=None)
                response.raise_for_status()
                return response.json()
            except Exception as err:
                raise err
