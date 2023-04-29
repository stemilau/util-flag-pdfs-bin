from concurrent.futures import ThreadPoolExecutor, as_completed

import pdf_and_io_tools
from pdf_and_io_tools.check import PdfProcessor
from pdf_and_io_tools.util import DataFrameWriter, parseArgs, processInputPath

def main() -> None:
    pdf_processor = PdfProcessor()
    df_writer = DataFrameWriter()
    no_pdfs = int()

    args = parseArgs()
    input_path = processInputPath(args.path_target)

    # ocr_vendors = readOcrVendors()
    with ThreadPoolExecutor() as executor:
        results = []
        print("...Waiting for pdfs to be processed...")
        for file_name in input_path.iterdir():
            if file_name.match('*.pdf'):
                no_pdfs += 1
                results.append(executor.submit(pdf_processor.processPdf, file_name))

        for p in as_completed(results):
            proc_result = p.result()
            df_writer.appendEntryDict(proc_result[0], proc_result[1])
    print(f"...Processing was successful: {no_pdfs} pdf files were checked...")
    df_writer.generateOutput(args.output_filename, input_path)

if __name__ == '__main__':
    main()