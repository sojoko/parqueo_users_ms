import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.admins_service import AdminsService
from schemas.admins import Admins, ChangeStatusRequest

mock_admin_data = Admins(
    name="AdminTest",
    last_name="AdminLast",
    document="987654321"
)

mock_admin_response = {
    'id': 1,
    'name': 'AdminTest',
    'last_name': 'AdminLast',
    'document': 987654321,
    'roll': 'admin'
}

mock_change_status_request = ChangeStatusRequest(
    id=1,
    status_id=2
)

class TestAdminsService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = AdminsService(repository=self.mock_repo)

    def test_create_admin_success(self):
        self.mock_repo.create_admin.return_value = True
        result = self.service.create_admin(mock_admin_data)
        assert result["message"] == "El usuario Admin fue regitrado correctamente"

    def test_create_admin_already_exists(self):
        self.mock_repo.create_admin.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.create_admin(mock_admin_data)
        assert exc.value.status_code == 400

    def test_get_all_admins(self):
        self.mock_repo.get_all_admins.return_value = [mock_admin_response]
        result = self.service.get_all_admins()
        assert isinstance(result, list)
        assert result[0]['id'] == 1

    def test_update_admin_success(self):
        self.mock_repo.update_admin.return_value = True
        result = self.service.update_admin(1, mock_admin_data)
        assert result["message"] == "El usuario administrador fue actualizado correctamente"

    def test_update_admin_not_found(self):
        self.mock_repo.update_admin.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.update_admin(1, mock_admin_data)
        assert exc.value.status_code == 404

    def test_get_admin_by_id_success(self):
        from types import SimpleNamespace
        mock_admin = SimpleNamespace(**mock_admin_response)
        self.mock_repo.get_admin_by_id.return_value = mock_admin
        result = self.service.get_admin_by_id(1)
        assert result['id'] == 1
        assert result['roll'] == 'admin'

    def test_get_admin_by_id_not_found(self):
        self.mock_repo.get_admin_by_id.return_value = None
        with pytest.raises(HTTPException) as exc:
            self.service.get_admin_by_id(1)
        assert exc.value.status_code == 404

    def test_change_admin_status_success(self):
        self.mock_repo.change_admin_status.return_value = True
        result = self.service.change_admin_status(mock_change_status_request)
        assert result["message"] == "El estado del administrador fue actualizado correctamente"

    def test_change_admin_status_not_found(self):
        self.mock_repo.change_admin_status.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.change_admin_status(mock_change_status_request)
        assert exc.value.status_code == 404

