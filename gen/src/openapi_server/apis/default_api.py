# coding: utf-8

from typing import Dict, List  # noqa: F401
import re
# import starlette


from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status, HTTPException,
)

from gen.src.openapi_server.models.extra_models import TokenModel  # noqa: F401
from gen.src.openapi_server.models.column_schema import ColumnSchema
from gen.src.openapi_server.models.column_type import ColumnType
from gen.src.openapi_server.models.database_create_post201_response import DatabaseCreatePost201Response
from gen.src.openapi_server.models.database_create_post_request import DatabaseCreatePostRequest
from gen.src.openapi_server.models.edit_value_location import EditValueLocation
from gen.src.openapi_server.models.table_schema import TableSchema

from db_cust import *

router = APIRouter()
database = None


def check_db_none():
    if database is None:
        raise HTTPException(status_code=400, detail='Database is not created')


def check_table_exists(tableId):
    try:
        global database
        table = database.get_table(tableId)
    except Exception as ef:
        raise HTTPException(status_code=400, detail=str(ef))

    return table


@router.post(
    "/database/create",
    responses={
        201: {"model": DatabaseCreatePost201Response, "description": "Database has been created"},
        400: {"description": "An error occurred during database creation."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_create_post(
        response: Response,
        database_create_post_request: DatabaseCreatePostRequest = Body(None, description=""),
) -> DatabaseCreatePost201Response:
    """Create an empty database"""
    db_name = database_create_post_request.database_name
    pattern = re.compile("[a-zA-Z]")
    if not pattern.match(db_name):
        raise HTTPException(status_code=400, detail="Bad request!")
    global database
    database = Database(db_name)

    response.status_code = 201
    response_data = DatabaseCreatePost201Response(
        database_name=database_create_post_request.database_name
    )
    return response_data


@router.post(
    "/database/table/create/",
    responses={
        201: {"model": TableSchema, "description": "Table created!"},
        400: {"description": "Such a table can&#39;t be created."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_create_post(
        response: Response,
        table_schema: TableSchema = Body(None, description="")
) -> TableSchema:
    """Create a new table"""

    check_db_none()
    try:
        table = Table(table_schema.table_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        global database
        database.add_table(table)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response.status_code = 201
    return table_schema


@router.post(
    "/database/load_database",
    responses={
        201: {"description": "Database has been loaded"},
        400: {"description": "An error occurred during loading the database"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_load_database_post(
        response: Response
) -> None:
    """Load saved database. It will override the current one."""
    global database
    try:
        database = Database.load_pickle()
    except Exception as f:
        raise HTTPException(status_code=400, detail=str(f))

    response.status_code = 201


@router.post(
    "/database/save_database",
    responses={
        201: {"description": "Database has been saved"},
        400: {"description": "An error occurred during database saving."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_save_database_post(
        response: Response
) -> None:
    """Save database to a file"""
    check_db_none()
    global database
    try:
        Database.save_pickle(database)
    except Exception as f:
        raise HTTPException(status_code=400, detail=str(f))

    response.status_code = 201

@router.delete(
    "/database/table/{tableId}/delete_duplicates",
    responses={
        204: {"description": "Deletion successful"},
        400: {"description": "An error occurred during deletion."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_delete_duplicates_delete(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
) -> None:
    """Delete duplicates of the rows in the Table"""
    check_db_none()
    table = check_table_exists(tableId)
    table.delete_duplicates()

    response.status_code = 204


@router.post(
    "/database/table/{tableId}/add_column",
    responses={
        201: {"model": ColumnSchema, "description": "Column created!"},
        400: {"description": "Bad request."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_add_column_post(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
        request_body: Dict[str, ColumnType] = Body(None, description=""),
) -> List[str]:
    """Add column to the specified table."""
    check_db_none()
    table = check_table_exists(tableId)
    """
    t_columns = [col.name for col in table.columns]
    for cname in request_body.keys():
        if cname not in t_columns:
            raise HTTPException(status_code=400, detail=f'Column {cname} is not present in the table')
    """
    # actual addition
    try:
        for name, ctype in request_body.items():
            column = Column(name, ctype)
            table.add_column(column)
    except Exception as ef:
        raise HTTPException(status_code=400, detail=str(ef))

    response.status_code = 201
    return [col.name for col in database.get_table(tableId).columns]


@router.post(
    "/database/table/{tableId}/add_row",
    responses={
        201: {"description": "Added."},
        417: {"description": "Some columns are not present in the table"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_add_row_post(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
        row_dict: Dict[str, str] = Body(None, description=""),
) -> None:
    """Add row to the specified table"""
    check_db_none()
    table = check_table_exists(tableId)

    for cname in row_dict.keys():
        if cname not in [col.name for col in table.columns]:
            raise HTTPException(status_code=417)

    table_str_to_column = {col.name: col for col in table.columns}

    row_col_dict = {}
    for cname, val in row_dict.items():
        key = table_str_to_column[cname]
        row_col_dict[key] = val
    try:
        row = Row(row_col_dict)
        table.add_row(row)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response.status_code = 201


@router.delete(
    "/database/table/{tableId}/{columnId}",
    responses={
        204: {"description": "Deletion successful"},
        400: {"description": "An error occurred during deletion."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_column_id_delete(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
        columnId: str = Path(None, description="Column Name"),
) -> None:
    """Delete column from the specified table."""
    check_db_none()
    table = check_table_exists(tableId)
    if columnId not in [col.name for col in table.columns]:
        raise HTTPException(status_code=400, detail=f'Column {columnId} is not present in the table')

    try:
        table.delete_column(columnId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response.status_code = 204


@router.delete(
    "/database/table/{tableId}",
    responses={
        204: {"description": "Deletion successful"},
        400: {"description": "An error occurred during deletion."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_delete(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
) -> None:
    """Drop table from database"""

    check_db_none()
    table = check_table_exists(tableId)
    global database
    database.delete_table(table)

    response.status_code = 204




@router.get(
    "/database/tables",
    responses={
        200: {"model": List[object], "description": "Success!"},
        400: {"description": "Bad request."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_tables_get(
        response: Response
) -> List[str]:
    """Get all tables."""
    check_db_none()


    """for row in table.rows:
        col_val_dict.append({'id': row.id, 'col_val': {col.name: val for col, val in row.col_val.items()}})
    a = {'table_name': table.name, 'table_columns': [col.name for col in table.columns],
         'table_rows': col_val_dict}
    print(a)"""
    response.status_code = 200
    return [str(table) for table in database.tables]



# return {'tables': table}

@router.patch(
    "/database/table/{tableId}/edit_value",
    responses={
        201: {"model": object, "description": "Update successful."},
        400: {"description": "Bad request"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_edit_value_patch(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
        edit_value_location: EditValueLocation = Body(None, description=""),
        value: str = Body(None, description="")
) -> object:
    """Update value for specified column name and row ID."""
    check_db_none()
    table = check_table_exists(tableId)
    try:
        table.edit_row_element(edit_value_location.column_name, edit_value_location.row_id, value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response.status_code = 201
    return value


@router.get(
    "/database/table/{tableId}",
    responses={
        200: {"model": object, "description": "Success!"},
        400: {"description": "Bad request."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_get(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
) -> object:
    """Get the specified table"""
    check_db_none()
    table = check_table_exists(tableId)

    response.status_code = 200
    return str(table)


@router.delete(
    "/database/table/{tableId}/row/{rowId}",
    responses={
        204: {"description": "Deletion successful"},
        400: {"description": "An error occurred during deletion."},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def database_table_table_id_row_id_delete(
        response: Response,
        tableId: str = Path(None, description="Table Name"),
        rowId: int = Path(None, description="Row Name"),
) -> None:
    """Delete row from the specified table."""
    check_db_none()
    table = check_table_exists(tableId)
    print(table.rows)
    try:
        table.delete_row(rowId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response.status_code = 204
