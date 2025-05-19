import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.parking_service import ParkingService
from schemas.parking import Parking

mock_parking_data = Parking(
    user_document=123456789,
    is_in_parking=1,
    vehicle_type=1
)

class TestParkingService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = ParkingService()
        self.service.repository = self.mock_repo

    def test_create_parking_success(self):
        self.mock_repo.create_parking.return_value = True
        result = self.service.create_parking(mock_parking_data)
        assert result["message"] == "El movimiento fue regitrado correctamente"

    def test_create_parking_already_exists(self):
        self.mock_repo.create_parking.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.create_parking(mock_parking_data)
        assert exc.value.status_code == 400
        assert "Ya existe un registro" in exc.value.detail

    def test_get_all_parking(self):
        self.mock_repo.get_all_parking.return_value = ["parking1", "parking2"]
        result = self.service.get_all_parking()
        assert result == ["parking1", "parking2"]

    def test_get_all_parking_counter(self):
        self.mock_repo.get_all_parking_counter.return_value = 5
        result = self.service.get_all_parking_counter()
        assert result == 5

    def test_get_parking_by_document(self):
        self.mock_repo.get_parking_by_document.return_value = {"user_document": 123456789}
        result = self.service.get_parking_by_document(123456789)
        assert result["user_document"] == 123456789

    def test_update_parking_success(self):
        self.mock_repo.update_parking.return_value = True
        result = self.service.update_parking(123456789, mock_parking_data)
        assert result["message"] == "El registro de parqueo fue actualizado correctamente"

    def test_update_parking_not_found(self):
        self.mock_repo.update_parking.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.update_parking(123456789, mock_parking_data)
        assert exc.value.status_code == 404
        assert "No se encontró un registro" in exc.value.detail
