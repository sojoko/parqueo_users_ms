import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.vigilante_service import VigilanteService
from schemas.vigilantes import Vigilantes, ChangeStatusRequest

mock_vigilante_data = Vigilantes(
    name="VigiTest",
    last_name="LanteTest",
    document="987654321"
)

mock_vigilante_response = {
    'id': 1,
    'name': 'VigiTest',
    'last_name': 'LanteTest',
    'document': 987654321,
    'role_id': 3
}

mock_change_status_request = ChangeStatusRequest(
    id=1,
    status_id=2
)

class TestVigilanteService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = VigilanteService()
        self.service.repository = self.mock_repo

    def test_create_vigilante_success(self):
        self.mock_repo.create_vigilante.return_value = {"message": "El usuario vigilante fue registrado correctamente"}
        result = self.service.create_vigilante(mock_vigilante_data)
        assert result["message"] == "El usuario vigilante fue registrado correctamente"

    def test_create_vigilante_already_exists(self):
        self.mock_repo.create_vigilante.side_effect = HTTPException(status_code=400, detail="El documento ya está registrado")
        with pytest.raises(HTTPException) as exc:
            self.service.create_vigilante(mock_vigilante_data)
        assert exc.value.status_code == 400
        assert "ya está registrado" in exc.value.detail

    def test_update_vigilante_success(self):
        self.mock_repo.update_vigilante.return_value = {"message": "El usuario vigilante fue actualizado correctamente"}
        result = self.service.update_vigilante(987654321, mock_vigilante_data)
        assert result["message"] == "El usuario vigilante fue actualizado correctamente"

    def test_update_vigilante_not_found(self):
        self.mock_repo.update_vigilante.side_effect = HTTPException(status_code=404, detail="Vigilante no encontrado")
        with pytest.raises(HTTPException) as exc:
            self.service.update_vigilante(987654321, mock_vigilante_data)
        assert exc.value.status_code == 404
        assert "Vigilante no encontrado" in exc.value.detail

    def test_get_vigilante_by_id_success(self):
        self.mock_repo.get_vigilante_by_id.return_value = mock_vigilante_response
        result = self.service.get_vigilante_by_id(1)
        assert result['id'] == 1
        assert result['role_id'] == 3

    def test_get_vigilante_by_id_not_found(self):
        self.mock_repo.get_vigilante_by_id.side_effect = HTTPException(status_code=404, detail="Vigilante no encontrado")
        with pytest.raises(HTTPException) as exc:
            self.service.get_vigilante_by_id(1)
        assert exc.value.status_code == 404
        assert "Vigilante no encontrado" in exc.value.detail

    def test_get_vigilante_by_document_success(self):
        self.mock_repo.get_vigilante_by_document.return_value = mock_vigilante_response
        result = self.service.get_vigilante_by_document(987654321)
        assert result['document'] == 987654321
        assert result['role_id'] == 3

    def test_get_vigilante_by_document_not_found(self):
        self.mock_repo.get_vigilante_by_document.side_effect = HTTPException(status_code=404, detail="Vigilante no encontrado")
        with pytest.raises(HTTPException) as exc:
            self.service.get_vigilante_by_document(987654321)
        assert exc.value.status_code == 404
        assert "Vigilante no encontrado" in exc.value.detail

    def test_get_all_vigilant(self):
        self.mock_repo.get_all_vigilant.return_value = [mock_vigilante_response]
        result = self.service.get_all_vigilant(1, 5)
        assert isinstance(result, list)
        assert result[0]['role_id'] == 3

    def test_change_vigilante_status_success(self):
        self.mock_repo.change_vigilante_status.return_value = {"message": "El estado del vigilante fue actualizado correctamente"}
        result = self.service.change_vigilante_status(mock_change_status_request)
        assert result["message"] == "El estado del vigilante fue actualizado correctamente"

    def test_change_vigilante_status_not_found(self):
        self.mock_repo.change_vigilante_status.side_effect = HTTPException(status_code=404, detail="El vigilante no fue encontrado")
        with pytest.raises(HTTPException) as exc:
            self.service.change_vigilante_status(mock_change_status_request)
        assert exc.value.status_code == 404
        assert "El vigilante no fue encontrado" in exc.value.detail
