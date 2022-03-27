import pdfquery
import pandas as pd

# First of all, we need to convert PDF into an Extensible Markup Language (XML), which includes data and metadata of a given PDF page.
pdf = pdfquery.PDFQuery('./Data/EsamiVari_CAIO.pdf')
pdf.load()
pdf.tree.write('pdfXML.txt', pretty_print=True)
