import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from services.users_service import UsersService
from schemas.usersLogin import User
from schemas.usersRegistry import UserRegistry
import bcrypt

mock_user_data = User(document=123456789, password="testpass")
mock_user_registry = UserRegistry(document=123456789, name="Test User", email="test@example.com", password="testpass", roll_id=2)
mock_user_response = {
    "document": 123456789,
    "name": "Test User",
    "email": "test@example.com",
    "roll_id": 2
}

class TestUsersService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = UsersService()
        self.service.repository = self.mock_repo

    def test_get_user_success(self):
        self.mock_repo.get_user_by_document.return_value = mock_user_response
        result = self.service.get_user(123456789)
        assert result == mock_user_response

    def test_get_user_not_found(self):
        self.mock_repo.get_user_by_document.return_value = None
        with pytest.raises(HTTPException) as exc:
            self.service.get_user(111)
        assert exc.value.status_code == 404

    def test_delete_user_success(self):
        self.mock_repo.delete_user_by_document_and_roll.return_value = True
        result = self.service.delete_user(123456789, 2)
        assert result["message"] == "Usuario eliminado con éxito"

    def test_delete_user_invalid_roll(self):
        with pytest.raises(HTTPException) as exc:
            self.service.delete_user(123456789, 99)
        assert exc.value.status_code == 400

    def test_delete_user_not_found(self):
        self.mock_repo.delete_user_by_document_and_roll.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.delete_user(123456789, 2)
        assert exc.value.status_code == 404

    def test_get_user_all_success(self):
        self.mock_repo.get_all_users.return_value = [mock_user_response]
        result = self.service.get_user_all()
        assert result == [mock_user_response]

    def test_get_user_all_not_found(self):
        self.mock_repo.get_all_users.return_value = []
        with pytest.raises(HTTPException) as exc:
            self.service.get_user_all()
        assert exc.value.status_code == 404

    def test_login_success(self, monkeypatch):
        class UserObj:
            document = 123456789
            password = bcrypt.hashpw(b"testpass", bcrypt.gensalt()).decode()
            roll_id = 2
            name = "Test User"
            email = "test@example.com"
        self.mock_repo.get_user_by_document_with_password.return_value = UserObj()
        monkeypatch.setattr(bcrypt, "checkpw", lambda pw, hpw: True)
        self.mock_repo.get_aprendiz_name_by_document.return_value = "Test User"
        result = self.service.login(mock_user_data)
        assert "access_token" in result

    def test_login_fail(self, monkeypatch):
        self.mock_repo.get_user_by_document_with_password.return_value = None
        with pytest.raises(HTTPException) as exc:
            self.service.login(mock_user_data)
        assert exc.value.status_code == 400

