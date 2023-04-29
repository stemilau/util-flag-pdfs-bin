import argparse
from os import getcwd
import PySimpleGUI as sg
from pathlib import Path
import pandas as pd


def parseArgs():
    print("...Waiting to fetch options and flags...")
    Parser = argparse.ArgumentParser(
        description=""" Utillity designed to distinguish between searcheable and non-searcheable pdf's in a directory.
                        by generating an output in the form of a csv/xlsx file, where the files are flagged as either,
                        searcheable or non-searcheable, located in the target directory.
                        """)
    Parser.add_argument(
        "output_filename",
        help=" Name of the output file, that stores the flagged vs non-flagged pdf files, as xlsx/csv. "
    )
    Parser.add_argument(
        "-p", "--path_target",
        metavar="PATH_OF_INPUT",
        help=""" Navigate to the given PATH_OF_INPUT of the target dir, where the utillity will sort the pdf files. If the
                 -p flag is not specified, the user will be prompted to choose from a window to select the dir.""",
        type=str,
        default=None
    )
    args = Parser.parse_args()
    return args


def dirBrowserGUI():
    working_dir = getcwd()

    layout = [
        [sg.Text("Choose a folder to process: ")],
        [sg.InputText(key="-FOLDER_PATH-"), sg.FolderBrowse(initial_folder=working_dir)],
        [sg.Button("Submit")]
    ]

    window = sg.Window("Browse the target folder", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Submit":
            target_dir_path = values["-FOLDER_PATH-"]
            window.close()
    return target_dir_path


def processInputPath(path_target_provided):
    if path_target_provided == None:
        input_path = dirBrowserGUI()
    else:
        input_path = path_target_provided
    return Path(input_path)


def readOcrVendors():
    ocr_vendors_lines = []
    with open('../OCR_VENDORS.txt', 'r') as ocr_vendors:
        ocr_vendors_lines = ocr_vendors.readlines()
    return ocr_vendors_lines


class DataFrameWriter():
    def __init__(self):
        self.search_list = list()

    def appendEntryDict(self, is_searcheable: bool, pdf_name):
        entry_dict = {"PDF_NAME": pdf_name, "IS_SEARCHEABLE": str(is_searcheable)}
        self.search_list.append(entry_dict)

    def generateOutput(self, output_filename, output_path: Path):
        print("...Generating output...")
        output_filename += ".xlsx"
        output_fullname = output_path / output_filename
        if output_fullname.is_file():  # checking if the output file already exists
            output_fullname.unlink()  # and deleting it to make room for the new one

        df = pd.DataFrame(self.search_list)
        df.to_excel(output_fullname)

        print(f"...Output was generated @ {output_fullname}")
