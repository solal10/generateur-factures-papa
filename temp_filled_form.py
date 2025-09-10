# Generated filled form script
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdfrw import PdfReader, PdfWriter, PageMerge

bg_path = "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"
overlay_path = "_text_overlay.pdf"
out_path = "FACTURE_21564321.pdf"

# Read background PDF to get dimensions
bg_pdf = PdfReader(bg_path)
page = bg_pdf.pages[0]
llx, lly, urx, ury = [float(x) for x in page.MediaBox]
page_width = urx - llx
page_height = ury - lly

# Create canvas for text overlay
c = canvas.Canvas(overlay_path, pagesize=(page_width, page_height))
c.setFont('Helvetica', 9)

c.drawString(130, page_height - 71.5, "21564321")
c.drawString(95, page_height - 96.5, "10/09/2025")
c.drawString(50, page_height - 214, "afasfgagasga")
c.drawString(50, page_height - 226, "agfsdfasgfagsag")
c.drawString(50, page_height - 238, "asfgasgagaga")
c.drawString(50, page_height - 250, "123451515123")
c.drawString(50, page_height - 262, "12351516563547457848")
c.drawString(355, page_height - 203, "afsjkgbajghkbajkb")
c.drawString(397, page_height - 227, "anbfskjasf jnakf")
c.drawString(393, page_height - 251, "12/12/12")
c.drawString(378, page_height - 263, "12/12/12")
c.drawString(60, page_height - 352, "asofjoagnaoinsgfoanfgoi[ngijasngkjangiajphnaohnoahinoiha[nhaonhaonhoin")
c.drawString(290, page_height - 352, "12")
c.drawString(360, page_height - 352, "12")
c.drawString(465, page_height - 352, "144.00")
c.drawString(60, page_height - 377, "test")
c.drawString(290, page_height - 377, "1")
c.drawString(360, page_height - 377, "11")
c.drawString(465, page_height - 377, "11.00")
c.drawString(465, page_height - 447, "155.00")
c.drawString(465, page_height - 475, "1")
c.drawString(465, page_height - 504, "1")
c.drawString(465, page_height - 529, "1")
c.drawString(465, page_height - 552, "158.00")
c.drawString(465, page_height - 572, "1")
c.drawString(465, page_height - 610, "157.00")

c.save()

# Merge text overlay with the acroform PDF
bg_pdf = PdfReader(bg_path)
overlay_pdf = PdfReader(overlay_path)

page_bg = bg_pdf.pages[0]
page_overlay = overlay_pdf.pages[0]

merger = PageMerge(page_bg)
merger.add(page_overlay).render()

PdfWriter(out_path, trailer=bg_pdf).write()
print('PDF generated successfully!')