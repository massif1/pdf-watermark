import PyPDF2
import sys
import os

pdf_input = os.path.realpath(sys.argv[1])
pdf_output = os.path.realpath(sys.argv[2])
pdf_watermark = os.path.realpath(sys.argv[3])


def check_args():
    """
    print('Number of arguments: ', len(sys.argv))
    print('The arguments are: ', str(sys.argv))
    print(f'Full path pdf_input > {pdf_input}')
    print(f'Full path pdf_output > {pdf_output}')
    print(f'Full path pdf_watermark > {pdf_watermark}')
    """

    if not os.path.exists(pdf_input):
        print(f'Folder in first argument, PDFs to watermark, does not exist => {pdf_input} \n\n exit')
        raise SystemExit

    if not os.path.exists(pdf_output):
        print('Output folder for watermarked PDFs in second Argument does not exist')
        os.makedirs(pdf_output)
        print(f'Created folder {pdf_output}')

    if not os.path.isfile(pdf_watermark) and pdf_watermark.endswith(".pdf"):
        print(f'Watermark PDF in third Argument does not exist => {pdf_watermark} \n\n exit')
        raise SystemExit


def pdf_watermarking():
    check_args()

    watermark = PyPDF2.PdfFileReader(pdf_watermark)
    watermark_page = watermark.getPage(0)

    # loop all pdfs
    for file in os.listdir(pdf_input):
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"):

            pdf_reader = PyPDF2.PdfFileReader(os.path.join(pdf_input, filename))
            pdf_writer = PyPDF2.PdfFileWriter()

            # merge every page in PDF with watermark
            for _ in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(_)
                page.mergePage(watermark_page)
                pdf_writer.addPage(page)

            # actual filename w/o path
            filename = os.path.basename(file)
            watermarked_pdf = f'{pdf_output}/{filename}'

            with open(watermarked_pdf, 'wb') as output:
                pdf_writer.write(output)
            print(f'Created {watermarked_pdf}')

    print('Done')


pdf_watermarking()
