# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_certguard
from pulpcore.client.pulp_certguard.api.contentguards_rhsm_api import ContentguardsRhsmApi  # noqa: E501
from pulpcore.client.pulp_certguard.rest import ApiException


class TestContentguardsRhsmApi(unittest.TestCase):
    """ContentguardsRhsmApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_certguard.api.contentguards_rhsm_api.ContentguardsRhsmApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        Create a rhsm cert guard  # noqa: E501
        """
        pass

    def test_delete(self):
        """Test case for delete

        Delete a rhsm cert guard  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List rhsm cert guards  # noqa: E501
        """
        pass

    def test_partial_update(self):
        """Test case for partial_update

        Partially update a rhsm cert guard  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a rhsm cert guard  # noqa: E501
        """
        pass

    def test_update(self):
        """Test case for update

        Update a rhsm cert guard  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
