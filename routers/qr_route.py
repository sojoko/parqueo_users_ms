from fastapi import APIRouter, HTTPException
import httpx
from models.qr import QR as QRModel
from schemas.qr import QR 
from qr import qr_generator
from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import matplotlib.pyplot as plt
import io
import tempfile


qr_router = APIRouter()


@qr_router.post("/api/v1/qr", tags=['QR'])
def create_qr(qr: QR, document: int):
    
    db = Session()
    document = int(document) 
    try_to_exist_qr = db.query(QRModel).filter(QRModel.user_document == document).first()
    
    if try_to_exist_qr:
        last_qr_date = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first().registry_date
        last_qr_image = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first().qr_image
        fecha_actual = datetime.now()
        time_limit = timedelta(hours=1)
        diferencia = fecha_actual - last_qr_date
        last_qr_image_decode = b64encode(last_qr_image).decode('utf-8')

        if diferencia < time_limit:
            return JSONResponse(status_code=200, content=jsonable_encoder(last_qr_image_decode))
    
    date_request = f'https://parqueo-frt.pages.dev/aprendiz-info?document={document}'
    qr_binary = b64decode(qr_generator(date_request=date_request))
    qr.qr = qr_binary
    qr.user_document = document
    
    new_qr = QRModel(
            qr_image = qr.qr,
            user_document=qr.user_document,             
        )
    db.add(new_qr)
    db.commit()
    
    qr_code_generated = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first().qr_image
    qr_code_generated_binary = b64encode(qr_code_generated).decode('utf-8')
    
    return JSONResponse(status_code=200, content=jsonable_encoder(qr_code_generated_binary))


@qr_router.get("/api/v1/generate-report", tags=['Report'], response_class=FileResponse)
async def generate_report():
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get('https://3.86.233.19:8000/api/v1/parking-all-counter')
            response.raise_for_status()
            data = response.json()

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
        c.drawString(100, height - 100, f"Capacidad total para motocicletas: {data['capacity_motorcycle']}")
        c.drawString(100, height - 120, f"Motocicletas actuales en el parqueadero: {data['motocycle_in_parking']}")
        c.drawString(100, height - 140, f"Parqueaderos disponibles para motocicletas: {data['actually_motorcycle_capacity']}")
       

        c.setFillColorRGB(0, 0, 0)     
        c.setFont("Helvetica-Bold", 14) 
        c.drawString(100, height - 160, f"Porcentaje de ocupacion de motocicletas: {data['percent_motorcycle_ocupation']:.2f}%")
        if data['percent_motorcycle_not_ocupation'] < 1:
            c.setFillColorRGB(1, 0, 0)
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 180, f"Porcentaje de disponibiliad para motocicletas: {data['percent_motorcycle_not_ocupation']:.2f}%")
        elif data['percent_motorcycle_not_ocupation'] >= 1 and data['percent_motorcycle_not_ocupation'] < 35:
            c.setFillColorRGB(1.0, 0.365, 0.0)
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 180, f"Porcentaje de disponibiliad para motocicletas: {data['percent_motorcycle_not_ocupation']:.2f}%")
        elif data['percent_motorcycle_not_ocupation'] >= 35:
            c.setFillColorRGB(0.0, 0.678, 0.196)
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 180, f"Porcentaje de disponibiliad para motocicletas: {data['percent_motorcycle_not_ocupation']:.2f}%") 
       
       
        c.setFont("Helvetica-Bold", 14)       
        c.setFillColorRGB(0.725, 0.090, 0.855)
        c.drawString(100, height - 220, f"Resumen bicicletas")         
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(100, height - 240, f"Capacidad total para bicicletas: {data['capacity_bycicle']}")       
        c.drawString(100, height - 260, f"Bicicletas actuales en el parqueadero: {data['bycicle_in_parking']}")
        c.drawString(100, height - 280, f"Parqueaderos disponibles para bicicletas: {data['actually_bycicle_capacity']}")      
        
        c.setFillColorRGB(0, 0, 0)     
        c.setFont("Helvetica-Bold", 14)        
        c.drawString(100, height - 300, f"Porcentaje de ocupacion para bicicletas: {data['percent_bycicle_ocupation']:.2f}%")
        
        if data['percent_bycicle_not_ocupation'] < 1:
            c.setFillColorRGB(1, 0, 0)
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 320, f"Portencaje de disponibilidad para bicicletas: {data['percent_bycicle_not_ocupation']:.2f}%")
        elif data['percent_bycicle_not_ocupation'] >= 1 and data['percent_bycicle_not_ocupation'] < 35:
            c.setFillColorRGB(1.0, 0.365, 0.0)
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 320, f"Portencaje de disponibilidad para bicicletas: {data['percent_bycicle_not_ocupation']:.2f}%")
        elif data['percent_bycicle_not_ocupation'] >= 35:
            c.setFillColorRGB(0.0, 0.678, 0.196)
            c.setFont("Helvetica-Bold", 14) 
            c.drawString(100, height - 320, f"Portencaje de disponibilidad para bicicletas: {data['percent_bycicle_not_ocupation']:.2f}%")
       

        def create_chart(data, labels, title):
            fig, ax = plt.subplots()
            ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title(title)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            plt.savefig(temp_file.name)
            plt.close(fig)
            return temp_file.name

        moto_data = [data['percent_motorcycle_ocupation'], data['percent_motorcycle_not_ocupation']]
        moto_labels = ['Plazas ocupadas', 'Plazas disponibles']
        moto_chart = create_chart(moto_data, moto_labels, 'Ocupacion de motocicletas')

        bike_data = [data['percent_bycicle_ocupation'], data['percent_bycicle_not_ocupation']]
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
   