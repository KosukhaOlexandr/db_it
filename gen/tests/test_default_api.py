# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.column_schema import ColumnSchema  # noqa: F401
from openapi_server.models.column_type import ColumnType  # noqa: F401
from openapi_server.models.database_create_post201_response import DatabaseCreatePost201Response  # noqa: F401
from openapi_server.models.database_create_post_request import DatabaseCreatePostRequest  # noqa: F401
from openapi_server.models.edit_value_location import EditValueLocation  # noqa: F401
from openapi_server.models.table_schema import TableSchema  # noqa: F401


def test_database_create_post(client: TestClient):
    """Test case for database_create_post

    
    """
    database_create_post_request = openapi_server.DatabaseCreatePostRequest()

    headers = {
    }
    response = client.request(
        "POST",
        "/database/create",
        headers=headers,
        json=database_create_post_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_load_database_post(client: TestClient):
    """Test case for database_load_database_post

    
    """

    headers = {
    }
    response = client.request(
        "POST",
        "/database/load_database",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_save_database_post(client: TestClient):
    """Test case for database_save_database_post

    
    """

    headers = {
    }
    response = client.request(
        "POST",
        "/database/save_database",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_create_post(client: TestClient):
    """Test case for database_table_create_post

    
    """
    table_schema = {"table_name":"tableName"}

    headers = {
    }
    response = client.request(
        "POST",
        "/database/table/create/",
        headers=headers,
        json=table_schema,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_add_column_post(client: TestClient):
    """Test case for database_table_table_id_add_column_post

    
    """
    request_body = [null]

    headers = {
    }
    response = client.request(
        "POST",
        "/database/table/{tableId}/add_column".format(tableId='table_id_example'),
        headers=headers,
        json=request_body,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_add_row_post(client: TestClient):
    """Test case for database_table_table_id_add_row_post

    
    """
    edit_value_location = {"row_id":1,"column_name":"columnName"}

    headers = {
    }
    response = client.request(
        "POST",
        "/database/table/{tableId}/add_row".format(tableId='table_id_example'),
        headers=headers,
        json=edit_value_location,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_column_id_delete(client: TestClient):
    """Test case for database_table_table_id_column_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/database/table/{tableId}/{columnId}".format(tableId='table_id_example', columnId='column_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_delete(client: TestClient):
    """Test case for database_table_table_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/database/table/{tableId}".format(tableId='table_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_delete_duplicates_delete(client: TestClient):
    """Test case for database_table_table_id_delete_duplicates_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/database/table/{tableId}/delete_duplicates".format(tableId='table_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_edit_value_patch(client: TestClient):
    """Test case for database_table_table_id_edit_value_patch

    
    """
    edit_value_location = {"row_id":1,"column_name":"columnName"}

    headers = {
    }
    response = client.request(
        "PATCH",
        "/database/table/{tableId}/edit_value".format(tableId='table_id_example'),
        headers=headers,
        json=edit_value_location,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_get(client: TestClient):
    """Test case for database_table_table_id_get

    
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/database/table/{tableId}".format(tableId='table_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_table_table_id_row_id_delete(client: TestClient):
    """Test case for database_table_table_id_row_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/database/table/{tableId}/{rowId}".format(tableId='table_id_example', rowId='row_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_database_tables_get(client: TestClient):
    """Test case for database_tables_get

    
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/database/tables",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

