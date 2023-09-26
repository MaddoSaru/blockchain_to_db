import blockchain
import fastapi

app = fastapi.FastAPI()
blockchain = blockchain.blockchain()


@app.get("/mine_block/")
def mine_block(data: str):
    if not blockchain.chain_validation():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )
    block = blockchain.mine_block(data=data)

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
