from typing import List
import blockchain
import fastapi
from utils.dml_functions import db_insert_block_data

app = fastapi.FastAPI()
blockchain = blockchain.blockchain()

def get_genesis_block():
    
    return blockchain.chain[0]

@app.get("/mine_block/")
def mine_block(data: str):
    if not blockchain.chain_validation():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )

    if len(blockchain.chain) == 1:
        db_insert_block_data(
            block = get_genesis_block(),
            genesis_block = get_genesis_block()
        )
    
    block = blockchain.mine_block(data=data)

    db_insert_block_data(
        block = block,
        genesis_block = get_genesis_block()
    )

    return block


@app.get("/get_blockchain/")
def get_blockchain():
    if not blockchain.chain_validation():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )

    return blockchain.chain


@app.get("/validate_blockchain/")
def validate_blockchain():
    return blockchain.chain_validation()
