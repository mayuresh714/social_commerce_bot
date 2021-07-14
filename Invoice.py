# import sqlite3
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import brown,grey,chocolate,black,turquoise

def generate_pdf(result):#ithe list pass kar
    l=1
    #l=result[1] #According to list parameters decide kar ani ashya kitipan list tayar karu shakto.
    pdf=canvas.Canvas(r"C:\Users\hp\repo\dynamic-main\IMAGE\Invoice.pdf")
    pdf.setFillColor(HexColor('#d8ebe4'))
    path = pdf.beginPath()
    path.moveTo(0 * cm, 0 * cm)
    path.lineTo(0 * cm, 30 * cm)
    path.lineTo(25 * cm, 30 * cm)
    path.lineTo(25 * cm, 0 * cm)
    pdf.drawPath(path, True, True)
    pdf.drawInlineImage(r"C:\Users\hp\repo\dynamic-main\IMAGE\logo.jpeg",350,650)
    pdf.setFont("Helvetica",30)
    pdf.setFillColor(HexColor("#7c9473"))
    pdf.setFontSize(40)
    pdf.drawCentredString(90,770,"INVOICE")
    pdf.setFont("Helvetica", 20)
    pdf.setFillColor(HexColor("#7c9473"))
    pdf.drawCentredString(80,730,"Invoice No:23153")#Ithe pan list chya according value pass kar ani string remove kar
    pdf.drawCentredString(45, 690, "Address:")
    pdf.setFillColor(HexColor("#62959c"))
    pdf.drawCentredString(130,670,"100,near PICT,Pune-411043")
    pdf.drawCentredString(130,630,"GSTIN : 07AABCS1429B1Z")
    pdf.setFillColor(HexColor("#7c9473"))
    pdf.drawCentredString(90,590,"Customer Details:")
    pdf.drawCentredString(60,560,"Phone NO:")
    pdf.setFillColor(HexColor("#62959c"))
    pdf.drawCentredString(170, 560, "9307840886")
    pdf.setFillColor(HexColor("#7c9473"))
    pdf.drawCentredString(55, 530, "Id")
    pdf.drawCentredString(140, 530, "Item")
    pdf.drawCentredString(230, 530, "Price")
    pdf.drawCentredString(330, 530, "Quantity")
    pdf.drawCentredString(430, 530, "Total")
    count=0
    total=0
    for i in range(1,l+1):#Ithe fakt number of items pass kar mi consider kelay l[0]
        pdf.setFillColor(HexColor("#62959c"))
        pdf.drawCentredString(55, 500-count, str(result[0][0]))#According to list parameters pass kar id,item,price,quantity,total.
        pdf.drawCentredString(140, 500-count, str(result[0][1]))
        pdf.drawCentredString(230, 500-count, str(result[0][2]))
        pdf.drawCentredString(330, 500-count, str(result[0][3]))
        pdf.drawCentredString(430, 500-count, str(result[0][4]))
        total=total+result[0][4]
        count=count+30
    pdf.setFillColor(HexColor("#62959c"))
    pdf.drawCentredString(330,500-count,"Total")
    pdf.drawCentredString(430,500-count,str(total))
    pdf.save()
    
x=[["12","vim","10","2",20]]
generate_pdf(x)
