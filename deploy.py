from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.8.0")

with open("./simpleStorage.sol", "r") as file:
    simpleStoreFile = file.read()


# compling the solidity code

compiled_solidity = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simpleStoreFile}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# print(compiled_solidity)
# writing the output i.e ABI to a file first import the json library
# write it first then dump it as a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_solidity, file)


# get bytecode
bytecode = compiled_solidity["contracts"]["simpleStorage.sol"]["store"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_solidity["contracts"]["simpleStorage.sol"]["store"]["abi"]

# print(abi)
#####How to connect to ganache   127.0.0.1:8545  https://sepolia.infura.io/v3/d8d36e88746f42e3ad62e068d3d47a8f
w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/d8d36e88746f42e3ad62e068d3d47a8f")
)

# infura chainID = 11155111
chain_id = 11155111

my_address = "0x4346a79828297d42F859B4cd9276A8d0e85Fc6B6"
private_key = os.getenv("MY_PRIVATE_KEY")
# "0x350d9733443e2a4971ba37b652b97e1174d72dc9e08535ce268b68f7ca35373a"
print(private_key)
# print(os.getenv("PRIVATE_KEY_2"))

storage = w3.eth.contract(abi=abi, bytecode=bytecode)

# print(storage)

nonce = w3.eth.get_transaction_count(my_address,"latest")
# print(nonce)

# HOW TO DEPLOY A SMART CONTRACT
# 1.BUID A TRANSACTION
# 2.SIGN A TRANSCATION
# 3.SEND A TRANSACTION

# 1. BUID A TRANSACTION
#####This error has cost me days "chainId is written as so not chain_id" so it is default
transaction = storage.constructor().build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2. SIGNING A TRANSACTION
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)

print("Deploying contract....................")

# 3. SEND A TRANSACTION
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# code has to wait for a few seconds to execute
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed!!!!!!!!!!!!!!!!!")

# Interacting with contracts now
# 1. ABI
# 2. ADDRESS
storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> call is made but no effect to contract
# transact -> make a state change to the contract

print(storage.functions.getBack().call())
# print(storage.functions.getBack())

######How to build a transaction contract##################
# 1.Build it
print("Updating Contract..............")
print(nonce)
print("Current Nonce:", nonce)
store_transaction = storage.functions.returnNumber(130).build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "gas": 2000000,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
# 2.sign it
signed_txn_two = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
# 3.send it
send_tx_hash_two = w3.eth.send_raw_transaction(signed_txn_two.rawTransaction)
##lastly delay the transaction abit to get it on the blockchain
tx_receipt_two = w3.eth.wait_for_transaction_receipt(send_tx_hash_two)

print("Updated!!!!!!!!!!!!!!!!!!!")
# print(storage.functions.returnNumber(18).call())
# print(storage.functions.getBack().call())
print(storage.functions.getBack().call())
