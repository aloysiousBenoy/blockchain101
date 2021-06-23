# Create a blockchain
import hashlib
import datetime
import json
from flask import Flask, jsonify

# Building a blockchain.
class Blockchain:
    # initialize a new blockchain;
    def __init__(self):
        # Create an empty list of blocks
        self.chain=[]
        # create the genesis block
        self.create_block(proof = 1,previous='0')        

    def create_block(self,proof,previous):
        # Define a block with the data.
        block ={
        'index':len(self.chain)+1,
        'timestamp':str(datetime.datetime.now()),
        'proof':proof,
        'previous_hash':previous,
        'data':"Sample data"
        }
        # Append the block to our chain.
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        proof_valid = False
        while proof_valid is False:
            # Calculate the hexadecimal sha256 sum using the pervious proof and the currently selected proof
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            # If passes minimimum condition, accept the proof

            if hash_operation[:4]=="0000":
                
                proof_valid = True
            else:
                # Else increment and repeat 
                new_proof+=1
        return new_proof
    def hash(self , block):
        # Dumb the dictionary/ json data as a string
        encoded_block = json.dumps(block,sort_keys=True).encode()
        # Hash the block and return the hex value
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):
        prev_block = chain[0]
       
        for block in chain[1::]:
            if block['previous_hash'] != self.hash(prev_block):
                # Return false if the hashes of the previous block and
                # prev hash in the current block are same
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_op = hashlib.sha256(str(proof**2-prev_proof**2).encode()).hexdigest()
            if hash_op[:4]!= '0000':
                # Return false if current block has invalid PoW
                return False
            prev_block = block
        # Return true if all blocks are valid 
        return True



# Mining blocks

app  = Flask(__name__)


# Create an object of the blockchain class we made
blockchain = Blockchain()


# Define a new route to mine blocks 
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    prev_proof = prev_block["proof"]
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof,prev_hash)
    response = {"message":"congratulations, you've just mined a block",
        "index":block["index"],
        "timestamp":block["timestamp"],
        "proof":block["proof"],
        "previous_hash":block["previous_hash"]
        }
    return jsonify(response),200

# Define a route to get block chain
@app.route('/get_chain',methods = ['GET'])
def get_chain():
    res = {
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(res), 200

@app.route('/is_valid',methods=['GET'])
def is_valid():
    valid_chain = blockchain.is_chain_valid(blockchain.chain)
    
    
    if valid_chain:
        return jsonify({"valid":True,"message":"The blockchain is valid."}), 200
    else : 
        return jsonify({"valid":False,"message":"The blockchain is not valid."}),500


app.run(host='0.0.0.0',port= 5000)