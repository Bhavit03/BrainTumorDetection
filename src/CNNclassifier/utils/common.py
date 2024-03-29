import os
from box.exceptions import BoxValueError
import yaml
from CNNclassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

"-> means what will be the return type"
"ConfigBox is a format of dictionary to easily access value of key"
"@ensureannotations ensures value is of specified type"

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    reads yaml file and return config box
    """ 
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file : {path_to_yaml} loaded succesfully")
            return ConfigBox(content)
    except BoxValueError:
        return ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_directories: list, verbose=True):
    for path in path_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path,'w') as f:
        json.dump(data,f,indent=4)

    logger.info(f"json file saved at : {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    with open(path) as f:
        content=json.load(f)

    logger.info(f"json file loaded successfully {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any,path : Path):
    joblib.dump(value=data,filename=path)
    logger.info(f"binary file saved at :{path}")

@ensure_annotations
def load_bin(path:Path) -> Any:
    data=joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb=round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

def decode_image(imgstring, filename):
    imgdata=base64.b64decode(imgstring)
    with open(filename,'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageintoBase64(croppedimgpath):
    with open(croppedimgpath,'rb') as f:
        return base64.b64encode(f.read())

