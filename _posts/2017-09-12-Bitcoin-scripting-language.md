<!-- --- -->
<!-- layout: post -->
<!-- comments: true -->
<!-- title:  "The bitcoin scripting language" -->
<!-- excerpt: "This post takes a deeper look at bitcoin transactions and th bitcoin scripting language." -->
<!-- date:   2017-09-12 -->
<!-- mathjax: true -->
<!-- --- -->

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

Let's strip most of the information which were added by the api and add ```vout_sz``` and ```vin_sz```.

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

There is the *transaction id* ```txid``` which is the hash of the transaction. A *version* ```version``` where the current version is specified. This can be used in the future, when there are changes have to be done in how transactions are speciied. Also there is a *locktime* ```locktime``` which specifies, before which the transaction can not become valid. Then there is ```vin_sz``` which counts the number of inputs. After that an array of inputs ```vin```. And the number of outputs ```vout_sz```, followed by the array of outputs ```vout```.

As you may have noticed, there are no keys ```signature``` or ```public-key```, what we would expect after our definition from the last time. That is because we have simplified the last time. What you have instead are ```scriptSig``` and ```scriptPubKey```. These are essentially code snippets of the *Bitcoin scripting language* simply called *Script*.

Script is a very small language with only the possibility of 256 instructions. Each of them is represented by one byte. Additionaly *Script* is by design not *turing-complete* (it cannot compute arbitrarily powerful functions), since the nodes which verify a transaction will have to execute the code snippets as we will see in a moment. So there should not be the possibility to build infinite loops.

*Script* is a stack based language, i.e. every instruction is executed once in a linear manner. Additionaly there is a memory, called *stack*, where we can push data to and pull data from. So let's take a closer look at one ```scriptPubKey``` and the corresponding ```scriptSig``` from a later transaction:

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

The ```OP_*``` are *Opcodes* they represent a instruction of script. The other lines in the above script are simply some kind of data. When data appears in a script it is simply an instruction to push that data on top of the stack. Before we "execute" the above script lets take a quick look at the *Opcodes* that we need for this script:


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
return: ```True```

---

So Basically as you could see executing these script validated the transaction on base of a public-key-signature-check, similar to the definition from the last time. The big pro of having script is theoretically, that we are able to build more complex ```scriptSig``` and ```scriptPubKey```, to achieve more complex behaviours. For example we can make an output be only spendable when a whole group of *private-keys* sign the spent-transaction. Or we could write some arbitrary data into the blockchain. 

Let's take a look at other things we can do with script and the bitcoin protocol in general.


## Examples 

### proof of burn
A *proof-of-burn* is a ```scriptPubKey```, which ensures, that there exists no ```scriptSig``` such that ```scriptSig+scriptPubKey``` executes succesful. In other words, the ```scriptPubKey``` guarentees, that there is now way to spend the coins, which where send to it. The coins are unusable, they are burned. 

The easiest way to achieve this, is to use the ```OP_RETURN``` opcode at the beginning of ```scriptPubKey```. This opcode simply throws an error. So it doesnt matter, what's in the ```scriptSig```, if ```scriptSig``` itself doesn't throw any errors, ```OP_RETURN``` will be executed and throws an error, invalidating the input. 

Another thing we can do with ```OP_RETURN``` is to store some arbitrary data (up to 80 byte) in the blockchain. We do this by burning a little amount of coins, sending them to a ```scriptPubKey```, containing our data. For example:

```
OP_RETURN
<our data>
```

Notice that we could use any other ```scriptPubKey``` and write our data in it, since we dont't care if it is spendable or not. But using ```OP_RETURN``` shows the *miners* that this output can never be redeemed, allowing them to forget about it. Thats good style since it doesn't bloat the data you have to keep track of when mining.

### pay-to-script-hash
Since the ```scriptPubKey``` and ```scriptSig``` have to match up in order to redeem the output, it can get really complicated for the user to send coins to someone who uses something different than a standard address. The user would have to specify the ```scriptPubKey``` exactly for the purposes of the receiver. This is not very handy and thats why the bitcoin community came up with the following solution.

There is the possibility of sending coins to the *hash* of a *script* instead of, for example a *public-key*. This is called *Pay-to-script-hash*. In order to redeem the output, you have to provide a script which hashes to the value specified in ```scriptPubKey``` in addition to executing valid, when providing additional data.

Let's take a look of sending coins to 2 of 3 multisig script address: 

The ```scriptPubKey``` is very simple and looks like this:

```scriptPubKey```:

```
OP_HASH160
<Hash of the redeem script>
OP_EQUAL
```

The ```scriptSig```, together with the ```redeem_script``` is relatively complicated, but that is nothing the sender has to care about. He only needs the hash of the redeem script.

```scriptSig```:

```
OP_0
<A's signature> 
<B's or C's signature>
<redeem script as data>
```

```redeem_script```:

```
OP_2
<A's pubkey>
<B's pubkey>
<C's pubkey>
OP_3
OP_CHECKMULTISIG 
```

Executing this will success, when the signature of *A* and one of *B* and *C* is provided correclty, together with the redeem script. 
```OP_2``` and ```OP_3``` are just pushing these numbers to the stack, to specify the input sizes of 3 *Public-keys* and two *signatures* needed to validate for ```OP_CHECKMULTISIG```. ```OP_0``` is to compensate a bug in the ```OP_CHECKMULTISIG```, which pulls an extra value of the stack and ignores it. The reaso why this isn't fixed is, that it would require a lot of coordination in the community, to change this simoultaniously, and its not considered that disrupting. 

Notice, that the ```redeem_script``` is pushed as raw data to the stack at first. Than after it was hashed and equals the hash specified in the ```scriptPubKey``` it is pushed again to the stack in its instuctional form. (This behaviour was a change to the bitcoin client and is specified in [BIP 16](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki)).

### escrow transactions

What we can also achieved with the above *2-of-3-Multisig* is a use case, where two parties can interact with each other using a intermediary, to resolve diputes.  Maybe out!!!

### Efficient micro-payments

Another interesting use case which also includes the ```locktime``` is a micropayment channel. It allows two parties, where one has to pay the other with multiple small payments, to wait until the end of a specific time to publish one transaction instead of a lot of little single transactions. 

This is achieved by the following protocol (the two paries are *A* and *B*, where *A* has to pay *B*):

* *A* and *B* agree on a ```max_value``` which is the highest amount, which *A* eventually pay to *B*
* *A* and *B* agree on a *2-of-2-multisignature-address* called ```escrow_address``` 
* Both sign a transaction which sends ```max_value``` from ```escrow_address``` to *A* with a ```locktime``` somewhere in the future.
* When *A* has to make a payment ```pay_1```, *A* signes a transaction which takes ```max_value``` from ```escrow_address``` as the input and pays ```pay_1``` to  *B* and the rest (```max_value - pay_1```) to *A* and sends it to *B*
* For each payment ```pay_n``` *A* signes a new transaction with ```escrow_address```  ```max_value``` as input and which pays $\sum_{i=1}^{n}$```pay_i``` to *B* and the rest to *A*.
* ...
* *B* signs the last transaction received from *A* and publishes it.

In case of any failure *A* can refund all of his coins in ```escrow_address``` after the ```locktime```. When *B* publishes the last transaction before the ```locktime``` exceeds, the *refund-transaction* will get invalid, as it is a double spend.

The downside of this protocol is that *denial-of-service* attacks could be used to prevent *B* from publishing the last transaction before the ```locktime```, which would result in *A* refunding his coins and doesn't paying *B* at all


## smart property

*Smart-poperty* is the idea of representing *ownership* with bitcoins. This is possible, because every bitcoin differs by his history and can therefore be distinguished from others. We could for example assign the ownership of our company to a specific bitcoin output and anounce this publicy. Now when we want to give shares of our company to someone we simply transfer the euivalent amount of the specified bitcoin output to the one we want to give the shares. Notice that when a transaction has several inputs and outputs containing coins which represent shares and some that don't, we have to specifiy in which output the shares go. This could be done by writing some metadata in an *proof-of-burn output*. 

A cool thing we can now accomplish is a *contract* directly in the Blockchain. If *A* wants to sell shares to *B*, *A* and *B* can create a transaction which takes the shares owned by *A* as one input and coins of *B* as another input. The outputs give the share to *B* and the coins to *A*. To make this transaction valid, both parites have to sign it with their *secret-keys*, just like a purchase-contract, but without the need of any lawyer. The execution is enforced by the bitcoin protocol itself. 


These examples are a form of *smart-contracts* in the general/traditional way, since they are contracts which are technically enforced.
Since bitcoins script is very small, the possibilities are limited, but yet powerful. Other cryptocurrencies/blockchain systems are using much more powerful languages. And can therefore build really complex smart contract. 
