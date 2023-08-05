from mock import Mock, patch, call
from tests.helpers.testbase import TestBase
from cerami.response import SaveResponse
from cerami.request import UpdateRequest
from cerami.request.mixins import Keyable, Returnable
from cerami.request.search_attribute import (
    UpdateExpressionAttribute,
    UpdateAction,
    DictAttribute)

class TestUpdateRequest(TestBase):
    def setUp(self):
        self.mocked_client = Mock()
        self.request  = UpdateRequest(
            tablename="test",
            client=self.mocked_client)

    def test_is_keyable(self):
        """it is keyable"""
        assert isinstance(self.request, Keyable)

    def test_is_returnable(self):
        """it is returnable"""
        assert isinstance(self.request, Returnable)

    def test_set(self):
        """it adds the SET attribute"""
        fake_expression = {'fake': True}
        self.request.update_expression = Mock()
        self.request.set(fake_expression)
        self.request.update_expression.assert_called_with('SET', fake_expression)
