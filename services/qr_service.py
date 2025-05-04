import httpx
from qr import qr_generator
from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.qr import QR
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import tempfile
from repository.qr_repository import QRRepository

class QRService:
    def __init__(self):
        self.repository = QRRepository()
    def create_qr(self, qr: QR, document: int):
        try:
            document = int(document) 
            try_to_exist_qr = self.repository.get_qr_by_document(document)

            if try_to_exist_qr:
                last_qr = self.repository.get_last_qr_by_document(document)
                last_qr_date = last_qr.registry_date
                last_qr_image = last_qr.qr_image
                fecha_actual = datetime.now()
                time_limit = timedelta(hours=1)
                diferencia = fecha_actual - last_qr_date
                last_qr_image_decode = b64encode(last_qr_image).decode('utf-8')

                if diferencia < time_limit:
                    return last_qr_image_decode

            # Generate new QR code
            date_request = f'https://parqueo.sojoj.com/aprendiz-info?document={document}'
            qr_binary = b64decode(qr_generator(date_request=date_request))

            qr_data = {
                "qr_image": qr_binary,
                "user_document": document
            }

            return self.repository.create_qr(qr_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def generate_report(self):
        try:
            parking = self.repository.get_all_parking()

            in_parking_motorcycle = 0
            in_parking_bycicle = 0
            out_of_parking_motorcycle = 0
            out_of_parking_bycicle = 0
            parking_motocycle_capacity = 3
            parking_bycicle_capacity = 20
            percent_motorcycle_not_ocupation = 0
            percent_motorcycle_ocupation = 0
            percent_bycicle_ocupation = 0
            percent_bycicle_not_ocupation = 0

            for doc in parking:
                if doc.vehicle_type == 1 and doc.is_in_parking == 1:
                    in_parking_motorcycle += 1
                elif doc.vehicle_type == 1 and doc.is_in_parking == 0:
                    out_of_parking_motorcycle += 1
                elif doc.vehicle_type == 2 and doc.is_in_parking == 1:
                    in_parking_bycicle += 1
                elif doc.vehicle_type == 2 and doc.is_in_parking == 0:
                    out_of_parking_bycicle += 1

            parking_actually_motorcycle_capacity = parking_motocycle_capacity - in_parking_motorcycle
            parking_actually_bycicle_capacity = parking_bycicle_capacity - in_parking_bycicle

            percent_motorcycle_ocupation = (in_parking_motorcycle * 100) / parking_motocycle_capacity
            percent_motorcycle_not_ocupation = 100 - percent_motorcycle_ocupation
            percent_bycicle_ocupation = (in_parking_bycicle * 100) / parking_bycicle_capacity
            percent_bycicle_not_ocupation = 100 - percent_bycicle_ocupation

            pdf_file = "report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica-Bold", 16)      
            c.drawString(75, height - 40, "Reporte de parqueadero - Parqueo API     " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            c.setFont("Helvetica-Bold", 14)        
            c.setFillColorRGB(0.2, 0.333, 1.0)
            c.drawString(100, height - 80, f"Resumen motocicletas")

            c.setFont("Helvetica", 14)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(100, height - 100, f"Capacidad total para motocicletas: {parking_motocycle_capacity}")
            c.drawString(100, height - 120, f"Motocicletas actuales en el parqueadero: {in_parking_motorcycle}")
            c.drawString(100, height - 140, f"Parqueaderos disponibles para motocicletas: {parking_actually_motorcycle_capacity}")


            c.setFillColorRGB(0, 0, 0)     
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 160, f"Porcentaje de ocupacion de motocicletas: {percent_motorcycle_ocupation:.2f}%")
            if percent_motorcycle_not_ocupation < 1:
                c.setFillColorRGB(1, 0, 0)
                c.setFont("Helvetica-Bold", 14) 
                c.drawString(100, height - 180, f"Porcentaje de disponibiliad para motocicletas: {percent_motorcycle_not_ocupation:.2f}%")
            elif 1 <= percent_motorcycle_not_ocupation < 35:
                c.setFillColorRGB(1.0, 0.365, 0.0)
                c.setFont("Helvetica-Bold", 14) 
                c.drawString(100, height - 180, f"Porcentaje de disponibiliad para motocicletas: {percent_motorcycle_not_ocupation:.2f}%")
            elif percent_motorcycle_not_ocupation >= 35:
                c.setFillColorRGB(0.0, 0.678, 0.196)
                c.setFont("Helvetica-Bold", 14) 
                c.drawString(100, height - 180, f"Porcentaje de disponibiliad para motocicletas: {percent_motorcycle_not_ocupation:.2f}%")


            c.setFont("Helvetica-Bold", 14)       
            c.setFillColorRGB(0.725, 0.090, 0.855)
            c.drawString(100, height - 220, f"Resumen bicicletas")         
            c.setFont("Helvetica", 14)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(100, height - 240, f"Capacidad total para bicicletas: {parking_bycicle_capacity}")
            c.drawString(100, height - 260, f"Bicicletas actuales en el parqueadero: {in_parking_bycicle}")
            c.drawString(100, height - 280, f"Parqueaderos disponibles para bicicletas: {parking_actually_bycicle_capacity}")

            c.setFillColorRGB(0, 0, 0)     
            c.setFont("Helvetica-Bold", 14)        
            c.drawString(100, height - 300, f"Porcentaje de ocupacion para bicicletas: {percent_bycicle_ocupation:.2f}%")

            if percent_bycicle_not_ocupation < 1:
                c.setFillColorRGB(1, 0, 0)
                c.setFont("Helvetica-Bold", 14) 
                c.drawString(100, height - 320, f"Portencaje de disponibilidad para bicicletas: {percent_bycicle_not_ocupation:.2f}%")
            elif 1 <= percent_bycicle_not_ocupation < 35:
                c.setFillColorRGB(1.0, 0.365, 0.0)
                c.setFont("Helvetica-Bold", 14) 
                c.drawString(100, height - 320, f"Portencaje de disponibilidad para bicicletas: {percent_bycicle_not_ocupation:.2f}%")
            elif percent_bycicle_not_ocupation >= 35:
                c.setFillColorRGB(0.0, 0.678, 0.196)
                c.setFont("Helvetica-Bold", 14) 
                c.drawString(100, height - 320, f"Portencaje de disponibilidad para bicicletas: {percent_bycicle_not_ocupation:.2f}%")


            def create_chart(data, labels, title):
                fig, ax = plt.subplots()
                ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                plt.title(title)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                plt.savefig(temp_file.name)
                plt.close(fig)
                return temp_file.name

            moto_data = [percent_motorcycle_ocupation, percent_motorcycle_not_ocupation]
            moto_labels = ['Plazas ocupadas', 'Plazas disponibles']
            moto_chart = create_chart(moto_data, moto_labels, 'Ocupacion de motocicletas')

            bike_data = [percent_bycicle_ocupation, percent_bycicle_not_ocupation ]
            bike_labels = ['Plazas ocupadas', 'Plazas disponibles']
            bike_chart = create_chart(bike_data, bike_labels, 'Ocupacion de bicicletas')


            c.drawImage(moto_chart, 20, height - 680, width=295, height=270)
            c.drawImage(bike_chart, 300, height - 680, width=295, height=270)

            c.save()

            return pdf_file
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error fetching data: {exc.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
