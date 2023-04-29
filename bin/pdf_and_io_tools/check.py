from os import getcwd, environ
from pathlib import Path
import subprocess
import pandas as pd
from io import StringIO


class PdfProcessor():
    def __init__(self, package_basedir=Path(getcwd())/'pdf_and_io_tools'):  # setting the package basedir of the project
        self.package_basedir = package_basedir
        environ['PATH'] += str(self.package_basedir)  # adding the binary of pdffonts to the environment PATH variable
        self.pdffonts = package_basedir / 'pdffonts.exe'

    # TODO: extract metadata and check it, and logs
    def extractFontsUsed(self, target_path: Path):
        p = subprocess.run([self.pdffonts, target_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True)  # running the pdffonts.exe on the specified target path
        raw_data = StringIO(p.stdout)  # extracting the raw_data from the standard output
        print(target_path.stem)
        print(p.stdout)
        df = pd.read_table(raw_data,
                           sep='\s+',
                           on_bad_lines='skip')  # parsing the raw_data using a pandas dataframe, where '\s+' specifies the separator as "one or more spaces"(REGEX)
        # and on_bad_lines='skip' is specified for trailing separators that may throw an exception, as pd is reading the raw_data
        font_names_arr = df['name'].values.tolist()  # extracting the first column of the dataframe into a list
        font_names_arr.pop(
            0)  # popping the first element of the list because it is a separator (multiple '-') in the ouput of the command
        return font_names_arr

    def processPdf(self, target_path: Path) -> tuple:
        pdf_name = target_path.stem
        is_searchable = bool()
        fonts_used = self.extractFontsUsed(target_path)
        if (len(fonts_used) == 0):
            is_searchable = False
        else:
            is_searchable = True

        return (is_searchable, pdf_name)
