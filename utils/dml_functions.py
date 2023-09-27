from utils.configs.general_configs import ddbb_config
import mysql.connector
from typing import Dict

def table_describe_dict(table_name: str) -> Dict:
    db = mysql.connector.connect(**ddbb_config)

    cursor = db.cursor()

    open_file = open(f"utils/queries/describe_table.sql", "r")
    query_str = open_file.read()
    format_query_str = query_str.format(table_name=table_name)

    cursor.execute(format_query_str)

    table_describe = cursor.fetchall()

    columns_structure = {}

    for column_description in table_describe:
        columns_structure[column_description[0]] = column_description[1].decode()

    return columns_structure

def generate_columns_values(
    describe_table : Dict,
    columns_values : Dict
) -> (str, str):
    columns = ""
    values = ""
    for column in columns_values:
        value = str(columns_values.get(column))
        if column != list(columns_values)[-1]:
            columns += column + ","
            values += (
                '"' + value + '",'
                if describe_table.get(column) in ["datetime", "char(200)"]
                else value + ","
            )
        else:
            columns += column
            values += (
                '"' + value + '"'
                if describe_table.get(column) in ["datetime", "char(200)"]
                else value
            )
    return (columns, values)
    


def db_insert_block_data(
    block : Dict,
    genesis_block : Dict,
):
    
    db = mysql.connector.connect(**ddbb_config)
    
    cursor = db.cursor()    
    
    open_file = open("utils/queries/insert_registers.sql", "r")
    query_str = open_file.read()

    columns_values = table_describe_dict(table_name = "blockchain")

    columns_values["block_index"] = block.get("index")
    columns_values["timestamp"] = block.get("timestamp")
    columns_values["genesis_block_flag"] = 1 if block.get("index") == 0 else 0
    columns_values["genesis_block_timestamp"] = genesis_block.get("timestamp")
    columns_values["data"] = block.get("data")
    columns_values["proof"] = block.get("proof")
    columns_values["previous_hash"] = block.get("previous_hash")
    
    columns, values = generate_columns_values(
        describe_table = table_describe_dict(table_name = "blockchain"),
        columns_values = columns_values
    )

    format_query_str = query_str.format(
        table_name = "blockchain",
        columns = columns,
        values = values
    )

    cursor.execute(format_query_str)

    db.commit()

    pass
