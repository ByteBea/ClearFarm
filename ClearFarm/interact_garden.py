from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3
import json

# ------------------------------------------------
# CONFIG — Inserisci qui i tuoi dati
# ------------------------------------------------
RPC = "https://api.avax-test.network/ext/bc/C/rpc"  # Fuji testnet
CHAIN_ID = 43113  # rete AVAX testnet

PRIVATE_KEY = "INSERISCI_LA_TUA_PRIVATE_KEY"  # es. "0xabcdef1234..."
CONTRACT_ADDRESS = "0xd00ae08403B9bbb9124bB305C09058E32C39A48c"

# ------------------------------------------------
# WEB3 CONNECTION
# ------------------------------------------------
w3 = Web3(Web3.HTTPProvider(RPC))
if not w3.is_connected():
    raise Exception(" Non connesso alla rete RPC AVAX")

# ------------------------------------------------
# LOAD CONTRACT ABI
# ------------------------------------------------
with open("/ortohub/ortohub/out/Garden.sol/Garden.json") as f:
    artifact = json.load(f)

ABI = artifact["abi"]
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=ABI
)

# ------------------------------------------------
# REQUEST MODELS
# ------------------------------------------------
class PlantPlotRequest(BaseModel):
    species: str
    organic_cert: bool
    token_uri: str

class WaterPlotRequest(BaseModel):
    plot_id: int
    amount: int

# ------------------------------------------------
# GENERIC TRANSACTION SENDER
# ------------------------------------------------
def send_tx(function_call):
    acct = w3.eth.account.from_key(PRIVATE_KEY)

    tx = function_call.build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 300000,
        "gasPrice": w3.to_wei(2, "gwei"),
        "chainId": CHAIN_ID,
    })

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {"tx_hash": tx_hash.hex(), "receipt": dict(receipt)}

# ------------------------------------------------
# FASTAPI SERVER ENDPOINTS
# ------------------------------------------------
app = FastAPI()

@app.post("/plant_plot")
def plant_plot_api(req: PlantPlotRequest):
    try:
        return send_tx(contract.functions.plantPlot(
            req.species,
            req.organic_cert,
            req.token_uri
        ))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/water_plot")
def water_plot_api(req: WaterPlotRequest):
    try:
        return send_tx(contract.functions.waterPlot(
            req.plot_id,
            req.amount
        ))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_plot/{plot_id}")
def get_plot_api(plot_id: int):
    try:
        return contract.functions.getPlot(plot_id).call()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
