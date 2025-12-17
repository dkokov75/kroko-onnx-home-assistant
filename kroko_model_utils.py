#!/usr/bin/env python3

import os
import json
import argparse
import requests
from tqdm import tqdm
from tabulate import tabulate

URL_KROKO_LICENSE_API = "https://license.kroko.ai/api/public/v1"

def kroko_get_model_data(lang, model_id):
    response = requests.get(f"{URL_KROKO_LICENSE_API}/models?language={lang}")
    response_data = response.json()

    for row in response_data:
        if row['model_id'] == model_id:
            return row

    return None

def kroko_get_pro_model_data(key, model_id):
    url = f"{URL_KROKO_LICENSE_API}/models?license={key}&model_id={model_id}"

    response = requests.get(url)
    return response.json()

def kroko_get_request(lang):
    response = requests.get(f"{URL_KROKO_LICENSE_API}/models?language={lang}")
    response_data = response.json()

    keys = ['name','type','language_iso','price','model_id']
    rows = [[item[k] for k in keys] for item in response_data]
    print(tabulate(rows,headers=keys,tablefmt='fancy_grid'))

def kroko_get_languages():
    response = requests.get(f"{URL_KROKO_LICENSE_API}/languages")
    response_data = response.json()

    keys = response_data[0].keys()
    rows = [[item[k] for k in keys] for item in response_data]
    print(tabulate(rows,headers=keys,tablefmt='fancy_grid'))

def kroko_get_download_file(model):
    current_dir = os.getcwd()
    filename = f"{current_dir}/models/stt/kroko_models/{model['name']}"

    try:
        with requests.get(model['url'], stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))

            with open(filename, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc=model['name']) as bar:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    bar.update(len(chunk))
    except Exception as e:
        print(f"Error: {e}")

def generate_yaml_string(language, stt_model, key=""):
    yaml_str = f"""services:
  homeassistant-kroko-stt:
    build:
      context: .
      args:
        LANGUAGE: "{language}"
        KROKO_STT_MODEL: "{stt_model}"
        KROKO_KEY: "{key}"
    container_name: kroko-onnx-stt-{language.lower()}
    ports:
      - 10400:10400
    restart: unless-stopped
"""
    return yaml_str

def create_lang_slink(lang):
    lang_dir = "models/stt/lang"
    target = "../kroko_onnx_streaming.py"
    link = f"{lang_dir}/{lang}"

    if not os.path.exists(link):
        os.symlink(target, link)
        print("Symlink created.")
    else:
        print("Symlink already exists.")

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=True,
        description="'kroko_model_utils.py' is command line tool",
        usage="./kroko_model_utils.py -x command option1 option2 ... optionN"
    )

    parser.add_argument(
        "-l",
        "--list",
#        type=str,
#        default="all",
        help="List all supported languages",
    )

    parser.add_argument(
        "-a",
        "--add",
        type=str,
        default="",
        help="Add choose language",
    )

    parser.add_argument(
        "--model_id",
        type=str,
        default="",
        help="Add choose model",
    )

    parser.add_argument(
        "--key",
        type=str,
        default="",
        help="",
    )

    return parser.parse_args()

def main():
    args = get_args()

    if args.list is not None:
        if "all" in args.list:
            kroko_get_languages()
        else:
            kroko_get_request(args.list)
    elif args.add is not None:
        yaml_str = None
        lang_short_link = args.add
        if args.model_id != "":
            model = kroko_get_model_data(lang_short_link, args.model_id)
            if model is not None:
                if model['type'] == "free":
                    kroko_get_download_file(model)
                    yaml_str = generate_yaml_string(lang_short_link, model['name'])
                elif model['type'] == "pro":
                    if args.key != "":
                        pro_model_data = kroko_get_pro_model_data(args.key, args.model_id)
                        kroko_get_download_file(pro_model_data[0])
                        yaml_str = generate_yaml_string(lang_short_link, pro_model_data[0]['name'], args.key)
                    else:
                        print("You should use '--key=kroko_license_key'!")
                if yaml_str is not None:
                    with open("docker-compose.yaml", "w") as f:
                        f.write(yaml_str)

                    create_lang_slink(lang_short_link)
            else:
                print("No model data!")

if __name__ == "__main__":
    main()