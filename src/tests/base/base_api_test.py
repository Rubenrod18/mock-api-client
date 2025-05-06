from tests.base.base_test import TestBase


class TestBaseApi(TestBase):
    def setUp(self):
        super().setUp()
        self.base_path = '/api'
