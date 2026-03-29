from fpdf import FPDF
from datetime import datetime

class ReporteService:
    @staticmethod
    def generar_pdf_productos(productos):
        pdf = FPDF()
        pdf.add_page()
        
        # Configuración de Título
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, "PIÑATERÍA BRYAN & KEVIN", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(190, 10, f"Reporte de Inventario - {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
        pdf.ln(10) # Espacio

        # Encabezado de Tabla
        pdf.set_fill_color(233, 30, 99) # Rosa de tu piñatería
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 12)
        
        pdf.cell(20, 10, "ID", 1, 0, 'C', True)
        pdf.cell(80, 10, "Producto", 1, 0, 'C', True)
        pdf.cell(40, 10, "Cantidad", 1, 0, 'C', True)
        pdf.cell(50, 10, "Precio", 1, 1, 'C', True)

        # Contenido de la Tabla (Usando tus Getters)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)
        
        for p in productos:
            pdf.cell(20, 10, str(p.get_id()), 1, 0, 'C')
            pdf.cell(80, 10, p.get_nombre(), 1, 0, 'L')
            pdf.cell(40, 10, str(p.get_cantidad()), 1, 0, 'C')
            pdf.cell(50, 10, f"$ {p.get_precio():.2f}", 1, 1, 'R')

        # Retornar el buffer del PDF
        return pdf.output(dest='S').encode('latin-1')