from PyPDF2 import PdfFileReader, PdfFileWriter
import os

def split_pdf(infn, outfn):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(open(infn, 'rb'))
    # 获取 pdf 共用多少页
    page_count = pdf_input.getNumPages()
    print(page_count)
    # 将 pdf 第五页之后的页面，输出到一个新的文件
    for i in range(5, page_count):
        pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))

def merge_pdf(infnList, outfn):
    pdf_output = PdfFileWriter()
    for infn in infnList:
        pdf_input = PdfFileReader(open(infn, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        print(page_count)
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))

if __name__ == '__main__':


    pdf_path = "C:\\Users\\theki\\Documents\\我的坚果云\\GuitarTabs\\歌单-草地音乐\\"
    paths = os.listdir(pdf_path)
    infnList = []
    for fileName in paths:
        path = pdf_path + fileName
        infnList.append(path)

    # infn = 'infn.pdf'
    outfn = pdf_path + 'album.pdf'
    merge_pdf(infnList, outfn)
    