import pytest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
from fastapi import HTTPException
from services.aprendices_service import AprendicesService
from models.aprendices import Aprendices as AprendizModel
from models.aprendices import EstadoAprendiz
from models.vehicles import Motocicleta as MotocicletaModel
from models.vehicles import Bicicleta as BicicletaModel
from schemas.aprendices import Aprendices, ChangeStatusRequest

# Mock data for testing
mock_aprendiz_data = Aprendices(
    name="Test",
    last_name="Apprentice",
    document="123456789",
    ficha="1234567",
    photo="test_photo.jpg",
    email="test@example.com",
    finish_date="2025-12-31"
)

mock_change_status_request = ChangeStatusRequest(
    document=123456789,
    state_id=2
)

class TestAprendicesService:
    def setup_method(self):
        self.service = AprendicesService()
        
    @patch('services.aprendices_service.Session')
    def test_get_all_aprendices(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_aprendiz = MagicMock()
        mock_aprendiz.__dict__ = {
            'id': 1,
            'name': 'Test',
            'last_name': 'Apprentice',
            'document': 123456789
        }
        mock_db.query.return_value.all.return_value = [mock_aprendiz]

        result = self.service.get_all_aprendices()

        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['name'] == 'Test'
        assert result[0]['roll'] == 'aprendiz'
        mock_db.query.assert_called_once_with(AprendizModel)
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_create_aprendiz_success(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = self.service.create_aprendiz(mock_aprendiz_data)

        assert result == {"message": "El aprendiz fue registrado exitosamente"}
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_create_aprendiz_duplicate_document(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock()

        with pytest.raises(HTTPException) as exc_info:
            self.service.create_aprendiz(mock_aprendiz_data)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "El documento ya existe"
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_get_aprendiz_by_id_success(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_aprendiz = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_aprendiz

        result = self.service.get_aprendiz_by_id(1)

        assert result == mock_aprendiz
        mock_db.query.assert_called_once_with(AprendizModel)
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_get_aprendiz_by_id_not_found(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.service.get_aprendiz_by_id(1)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "El aprendiz no fue encontrado"
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_get_aprendiz_by_document_success(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_aprendiz = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_aprendiz

        result = self.service.get_aprendiz_by_document(123456789)

        assert result == mock_aprendiz
        mock_db.query.assert_called_once_with(AprendizModel)
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_get_aprendiz_by_document_not_found(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.service.get_aprendiz_by_document(123456789)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "El documento no fue encontrado"
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_get_aprendiz_status_by_document_success(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_aprendiz = MagicMock()
        mock_aprendiz.state_id = 1
        mock_status = MagicMock()
        mock_status.estado = "Activo"
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_aprendiz, mock_status]

        result = self.service.get_aprendiz_status_by_document(123456789)

        assert result == "Activo"
        assert mock_db.query.call_count == 2
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_change_aprendiz_status_success(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_aprendiz = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_aprendiz

        result = self.service.change_aprendiz_status(mock_change_status_request)

        assert result == {"message": "El estado del aprendiz fue actualizado correctamente"}
        assert mock_aprendiz.state_id == 2
        mock_db.commit.assert_called_once()
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_change_aprendiz_status_not_found(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.service.change_aprendiz_status(mock_change_status_request)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "El documento no fue encontrado"
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_update_aprendiz_success(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_aprendiz = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_aprendiz

        result = self.service.update_aprendiz(123456789, mock_aprendiz_data)

        assert result == {"message": "El aprendiz fue actualizado correctamente"}
        assert mock_aprendiz.name == mock_aprendiz_data.name
        assert mock_aprendiz.last_name == mock_aprendiz_data.last_name
        assert mock_aprendiz.document == int(mock_aprendiz_data.document)
        assert mock_aprendiz.ficha == int(mock_aprendiz_data.ficha)
        assert mock_aprendiz.email == mock_aprendiz_data.email
        mock_db.commit.assert_called_once()
        mock_db.close.assert_called_once()
    
    @patch('services.aprendices_service.Session')
    def test_update_aprendiz_not_found(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.service.update_aprendiz(123456789, mock_aprendiz_data)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Aprendiz no encontrado"
        mock_db.close.assert_called_once()