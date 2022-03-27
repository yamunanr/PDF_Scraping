import pdfquery
import tabula as tb
import pandas as pd

# First of all, we need to convert PDF into an Extensible Markup Language (XML), which includes data and metadata of a given PDF page.
pdf = pdfquery.PDFQuery('./Data/EsamiVari_CAIO.pdf')
pdf.load()
pdf.tree.write('pdfXML.txt', pretty_print=True)


# Function to scrape data from pdf
def pdfscrape(df):
    # Extract each relevant information individually
    wbc = pdf.pq('LTTextLineHorizontal:overlaps_bbox("56.9, 757.808,  158.612, 769.808")').text()
    rbc = pdf.pq('LTTextLineHorizontal:overlaps_bbox("56.9,  730.208,  160.484, 742.208")').text()
    hgb = pdf.pq('LTTextLineHorizontal:overlaps_bbox("56.9, 702.608, 178.244, 714.608")').text()

    # Combined all relevant information into single observation
    page = pd.DataFrame({
        'wbc': wbc,
        'rbc': rbc,
        'hgb': hgb,
    }, index=[0])
    return page


pagecount = pdf.doc.catalog['Pages'].resolve()['Count']

master = pd.DataFrame()
for p in range(pagecount):
    pdf.load(p)
    page = pdfscrape(pdf)
    master = master.append(page, ignore_index=True)

master.to_csv('output.csv', index=False)
keyword =  pdf.pq('LTTextLineHorizontal:contains("{}")'.format("social security number"))[0]
x0 = float(keyword.get('x0',0))
y0 = float(keyword.get('y0',0)) - 10
x1 = float(keyword.get('x1',0))
y1 = float(keyword.get('y1',0)) - 10
ssn = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text()
