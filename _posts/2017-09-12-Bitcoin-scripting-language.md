---
layout: post
comments: true
title:  "The bitcoin scripting language"
excerpt: "This post takes a deeper look at bitcoin transactions and th bitcoin scripting language."
date:   2017-09-12
mathjax: true
---

Last time we introduced transactions. We defined them to have inputs and outputs, where there are *public-keys* specified in the *outputs* and *private-key-signatures* in the inputs. In bitcoin it is slightly different than that. Its much more powerful. So Lets take a look at a almost raw bitcoin transaction (a real raw bitcoin transaction is not human readable, this is the information from a bitcoin transaction in a more pretty json format. This is the output of the <https://blockexplorer.com> api): 

```json
{
  "txid": "90b18aa54288ec610d83ff1abe90f10d8ca87fb6411a72b2e56a169fdc9b0219",
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "18798f8795ded46c3086f48d5bdabe10e1755524b43912320b81ef547b2f939a",
      "vout": 0,
      "scriptSig": {
        "asm": "3045022100c1efcad5cdcc0dcf7c2a79d9e1566523af9c7229c78ef71ee8b6300ab59aa63d02201fe27c3e6374dd3a5425a577d9ca6ad8ff079800175ef9a44475bc98bcef21cf[ALL] 023b027d54ce8b6c730e0d5833f73aec6a5bae4efe04f57d2864a6a7df2af56e46",
        "hex": "483045022100c1efcad5cdcc0dcf7c2a79d9e1566523af9c7229c78ef71ee8b6300ab59aa63d02201fe27c3e6374dd3a5425a577d9ca6ad8ff079800175ef9a44475bc98bcef21cf0121023b027d54ce8b6c730e0d5833f73aec6a5bae4efe04f57d2864a6a7df2af56e46"
      },
      "sequence": 4294967295,
      "n": 0,
      "addr": "1GqpaRRvdX8HpqRUzg42v5GMPEoFDXV27Q",
      "valueSat": 168400000000,
      "value": 1684,
      "doubleSpentTxID": null
    }
  ],
  "vout": [
    {
      "value": "5.93100000",
      "n": 0,
      "scriptPubKey": {
        "hex": "76a9144b358739fc7984b8101278988beba0cc00867adc88ac",
        "asm": "OP_DUP OP_HASH160 4b358739fc7984b8101278988beba0cc00867adc OP_EQUALVERIFY OP_CHECKSIG",
        "addresses": [
          "17rfobSZ8Dj61c8sanhzzR76ADMjWYYpCP"
        ],
        "type": "pubkeyhash"
      },
      "spentTxId": "717b2f3e1b872aebe0cc64434dd0be9ccfa29d9f077c0f65bbaaa4a65fcc3b7d",
      "spentIndex": 3,
      "spentHeight": 286801
    },
    {
      "value": "1678.06900000",
      "n": 1,
      "scriptPubKey": {
        "hex": "76a91455368b388ccfe22a3f837c9eee93d053460db33988ac",
        "asm": "OP_DUP OP_HASH160 55368b388ccfe22a3f837c9eee93d053460db339 OP_EQUALVERIFY OP_CHECKSIG",
        "addresses": [
          "18mZn5VXoxcb6MbNKQj17bX4qYxNEU7SDe"
        ],
        "type": "pubkeyhash"
      },
      "spentTxId": "4982fa325c725749b63a883bc73e2c684d1502ada1c7076fb69b634c3ae5b0a3",
      "spentIndex": 0,
      "spentHeight": 288896
    }
  ],
  "blockhash": "0000000000000000bf3856e067ec21f4c30a8a859cc7ed7f2de9a2b579200639",
  "blockheight": 286731,
  "confirmations": 197946,
  "time": 1392828428,
  "blocktime": 1392828428,
  "valueOut": 1684,
  "size": 226,
  "valueIn": 1684,
  "fees": 0
}
```

Let's strip the information which were added by the api and add ```vout_sz``` and ```vin_sz```.

```json
{
  "txid": "90b18aa54288ec610d83ff1abe90f10d8ca87fb6411a72b2e56a169fdc9b0219",
  "version": 1,
  "locktime": 0,
  "vin_sz": 1,
  "vin": [
    {
      "txid": "18798f8795ded46c3086f48d5bdabe10e1755524b43912320b81ef547b2f939a",
      "vout": 0,
      "scriptSig": {
        "asm": "3045022100c1efcad5cdcc0dcf7c2a79d9e1566523af9c7229c78ef71ee8b6300ab59aa63d02201fe27c3e6374dd3a5425a577d9ca6ad8ff079800175ef9a44475bc98bcef21cf[ALL] 023b027d54ce8b6c730e0d5833f73aec6a5bae4efe04f57d2864a6a7df2af56e46",
        "hex": "483045022100c1efcad5cdcc0dcf7c2a79d9e1566523af9c7229c78ef71ee8b6300ab59aa63d02201fe27c3e6374dd3a5425a577d9ca6ad8ff079800175ef9a44475bc98bcef21cf0121023b027d54ce8b6c730e0d5833f73aec6a5bae4efe04f57d2864a6a7df2af56e46"
      },
    }
  ],
  "vout_sz": 2,
  "vout": [
    {
      "value": "5.93100000",
      "n": 0,
      "scriptPubKey": {
        "hex": "76a9144b358739fc7984b8101278988beba0cc00867adc88ac",
        "asm": "OP_DUP OP_HASH160 4b358739fc7984b8101278988beba0cc00867adc OP_EQUALVERIFY OP_CHECKSIG",
        "type": "pubkeyhash"
      },
    },
    {
      "value": "1678.06900000",
      "n": 1,
      "scriptPubKey": {
        "hex": "76a91455368b388ccfe22a3f837c9eee93d053460db33988ac",
        "asm": "OP_DUP OP_HASH160 55368b388ccfe22a3f837c9eee93d053460db339 OP_EQUALVERIFY OP_CHECKSIG",
        "type": "pubkeyhash"
      },
    }
  ],
  "valueOut": 1684,
  "size": 226,
  "valueIn": 1684,
  "fees": 0
}
```

There is the *transaction id* ```txid``` which is the hash of the transaction. A *version* ```version``` where the current version is specified. This can be used in the future, when there are changes have to be done in how transactions are speciied. Also there is a *locktime* ```locktime``` which specifies, when the transaction can be inlcuded in a block. Then there is ```vin_sz``` which counts the number of inputs. After that an array of inputs ```vin```. And then the number of outputs ```vout_sz``` and the array of outputs ```vout```.

As you may have noticed, there are no keys ```signature``` or ```public-key```, what we would expect after our definition from the last time. That is because we have simplified the last time. What you have instead are ```scriptSig``` and ```scriptPubKey```. These are essentially code snippets of the *Bitcoin scripting language* simply called *Script*.

Script is a very small language with only the possibility of 256 instructions. Each of them is represented by one byte. Additionaly *Script* is by design not *turing-complete* (it cannot compute arbitrarily powerful functions), since the nodes which verify a transaction will have to execute the code snippets as we will see in a moment. So there should not be the possibility to build infinite loops.

*Script* is a stacked based language, i.e. every instruction is executed once in a linear manner. So let's take a closer look at one ```scriptPubKey``` and the corresponding ```scriptSig``` from a later transaction:

```json
[
"scriptSig": {
        "asm": "304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e[ALL] 02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c",
        "hex": "48304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e012102f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c"
      },
"scriptPubKey": {
  "hex": "76a91455368b388ccfe22a3f837c9eee93d053460db33988ac",
  "asm": "OP_DUP OP_HASH160 55368b388ccfe22a3f837c9eee93d053460db339 OP_EQUALVERIFY OP_CHECKSIG",
  "type": "pubkeyhash"
}
]

```

We are only interested in the ```asm``` part, becasue that is the human readable form. In order for an input to be valid, what you have to do is concatenate ```scriptSig``` and ```scriptPubKey``` and if it executes succesful, the input is valid. So if we take our above *scripts* and concatenate them we get:

```
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
OP_DUP
OP_HASH160
55368b388ccfe22a3f837c9eee93d053460db339
OP_EQUALVERIFY
OP_CHECKSIG",
```

The ```OP_*``` are *Opcodes* they represent a instruction of script. The other lines in the above script are simply some kind of data. Before we "execute" the above script lets take a quick look at the *Opcodes* that we need for this script:


| OPCODE               | function                                                                                                                    |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| ```OP_DUP```         | Duplicates the item on top of the stack                                                                                     |
| ```OP_HASH160```     | Hashes the top item on the stack (first SHA-256 then RIPEMD-160)                                                            |
| ```OP_EQUALVERIFY``` | True if the top two items on the stack are equal. False otherwise (marks tx as invalid)                                     |
| ```OP_CHECKSIG```    | Takes the top two items of the stack and checks if the signature is a valid one for the current transaction and the pub-key |

Now we will execute the script above step by step:

script:
```
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
OP_DUP
OP_HASH160
55368b388ccfe22a3f837c9eee93d053460db339
OP_EQUALVERIFY
OP_CHECKSIG",
```

stack:
```
```
---
the First entry of the script was pushed to the stack. (This was a signature).

script:
```
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
OP_DUP
OP_HASH160
55368b388ccfe22a3f837c9eee93d053460db339
OP_EQUALVERIFY
OP_CHECKSIG",
```

stack:
```
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
```
---
The second entry of the script was also data, which were pushed to the stack (it was a public key)

script:
```
OP_DUP
OP_HASH160
55368b388ccfe22a3f837c9eee93d053460db339
OP_EQUALVERIFY
OP_CHECKSIG",
```

stack:
```
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
```
---
The top item of the stack was duplicated.

script:
```
OP_HASH160
55368b388ccfe22a3f837c9eee93d053460db339
OP_EQUALVERIFY
OP_CHECKSIG",
```

stack:
```
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
```
---
The top item was replaced by its hash.

script:
```
55368b388ccfe22a3f837c9eee93d053460db339
OP_EQUALVERIFY
OP_CHECKSIG",
```

stack:
```
55368b388ccfe22a3f837c9eee93d053460db339
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
```
---
The hash from the ```scriptPubKey``` was pushed to the stack.

script:
```
OP_EQUALVERIFY
OP_CHECKSIG",
```

stack:
```
55368b388ccfe22a3f837c9eee93d053460db339
55368b388ccfe22a3f837c9eee93d053460db339
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
```
---
The two hash values were compared, to verify, that the given public-key matches the one from ```scriptSig```

script:
```
OP_CHECKSIG",
```

stack:
```
02f6da6b206ba5f83566327407966263ce3c062ca0db1ba61eeab2db2032e7b06c
304502210080789d3375b6a28f44e8cbb8ec665d2ef74189c04001c9ca8444a666119ae0d7022030366d8451dd80761c075765002852e6629631f87b7ae50a4690d5f345bd9c2e
```
---
The signature was checked and the result (```True``` in this case) is returned.

script:
```
```

stack:
```
```
return:
```True```
---

So Basically as you could see executing these script validated the transaction on base of a public-key-signature-check, similar to the definition from the last time. The big pro of having script is theoretically, that we are able to build more complex ```scriptSig``` and ```scriptPubKey```, to achieve more complex behaviours. For example we can make an output be only spendable when a whole group of *private-keys* sign the spent-transaction. This is a very very simple *smart-contract*. Another *smart-contract* we can establish with script are micro-payment channels. These is some kind of protocol, where one party can pay another in multiple single micro payments and there is only the need to broadcast one transaction to the blockchain at the end. 

In general a *smart-contract* is one which is technically enforced. Since bitcoins script is very small, the possibilities are limited, but yet powerful. Other cryptocurrencies/blockchain systems are using much more powerful languages. And can therefore build really complex smart contract, which can build up to decentralized apps. 
