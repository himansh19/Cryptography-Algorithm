# Cryptography-Algorithm
I have used various **Cryptographic algorithms to make communication between client and server as secure as possible**, 
Here everything is done step by step and first I have talked about Symmetric Key encryption Techniques, Then moves to Public (Asymmetric) Encryption and then we understand the advantages & Disadvantages of Both and then combined both & used the concept of Signature to provide maximum security.
Some of the codes uses library (as we must have knowledge about them), but after that I have also implemented the same thing from scratch i.e a dummy hash function, Euclid algorithm for generating key in RSA.
Recommended to explore in order to get familiar with idea & Content.


  1. Simple Symmetric Key Cipher based on **just char shifting by key (Caesar)**. Having no multithreading means only one client communicate with one server.
  2. Implemented the Same Caesar Cipher but added the functionality of threading, now one server can communicate with multiple clients. Also there is one problem in previous Cipher that we are not dealing with space char while encrypting & decrypting, there we are getting n instead of space characted so have solved that problem also.

      Now above two are Symmetric Cipher but problem with them is that here we can
     **Determine key very easily**
     **same key is known to others(client & Server)** so not that much secured.
     Also Key Distribution through KDC (Key Distribution Centre) is not totally secured [Will later see Asymmetric can used for key distribution]
  4. Now we have come to **public key Cryptography i.e Asymmetric and used RSA(Rivest–Shamir–Adleman)**, in first case we have imported RSA library and used that, besides that both client and server know each other public key prior to connection.
  5. In next phase we have implemented RSA from scratch and keys are not known already but will be shared after the connection (key sharing not secure, will require **Certificates & Signatures** which is implemented later). Here implemented everything from key generation algorithm(GCD, Extended Euclid ALgo, Multiplicative inverse..) to sharing of keys.

       Now all was good until know but problem in Public key cryptography is cost, i.e it is **computationally expensive** and take larger time for encryption & Decryption.
       Also we encounter problem of how to **share Public key of one another in a secured manner**.
       Also there is no integrity, confidentiality & authentication present i.e **CIA violation**, as attacker can impersonate and send msg on behalf of other, or content present in msg can be altered, so how to ensure what is sent is being received, and how to authenticate one another.

     Solution to this problem is the use of Signatures (use concept of Hash behind) How ? 
     As Asymmetric encryption is computionally expensive, so we will only encrypt Hash of the msg (which is fixed size) using Asymmetric encryption (by priv key) [it is called signature] and rest of the message is send using Symmetric encryption by use of Symmetric Key.
     How they know symmetric Key? -> By use of **Digital Envelope** i.e encrypt symmetric also with assymetric encryption for session. 

     Now CIA Secured: **Confidentialty** -> Data cannot be read as used symmetric cryptogrpahy & symmetric key will change after every session and will be send after connection establishment.
               **Integrity** -> msg cannot be altered in way, if changed then hash of msg also change, so will know.
               **Authentication** -> as apply public key of sender on hash to decrypt hash, so will ensured that whosoever encrypt this hash has sender priv key and priv key is known only to sender so authenticated.

     Now problem of Key exchange that how will know each other public key also solved using application & concept of signature but instead of sender or receiver, Some third party which is known as **Certifying Authority** put signature(Hash of content of certificate encrypt with priv key of CA) on the certificate. Certificate content include information of public key and is known as public key certificate along with signature of CA.

  Here we have used Signature concept to provide CIA i.e every msg is send with it's hash taking use of both type of cryptography. In the same contrast key exchange can be implemented which is lot easier than that as only CA has to generate a certificate and put it's signature on that but we have not implemented here as become complex for you.
  5. Using the help of library implemented concept of **Digital signature** and used inbuilt functions for that.
  6. Have implemented everything from scratch and line by line generated signature from hashing of the content of every msg. Also not used inbuilt hash function, instead **make our own sample hash** for this lab.

Symmetric Cryptography(same key): ![image](https://github.com/himansh19/Cryptography-Algorithm/assets/89848299/9336849c-9095-4845-b526-49a91e8e1048)

Asymmetric Cryptography (Different Key): ![image](https://github.com/himansh19/Cryptography-Algorithm/assets/89848299/f21affb5-b400-4dfc-a8eb-a310fbcd75c4)

Digital Envelope (Encrypt Symmetric Key with Asymmetric Key and combine with data encrypted with symmetric key): ![image](https://github.com/himansh19/Cryptography-Algorithm/assets/89848299/7f13f4c3-f0d1-4d1b-9996-4912a52a75a0)

Digital Signature (Encrypt message hash with Asymmetric Encryption): ![image](https://github.com/himansh19/Cryptography-Algorithm/assets/89848299/cd6fa52e-9e20-4567-972e-867e1ba0338e)

Public Key Certificate (Special message with Special signature) i.e msg containing public key & information + Hash of this msg encrypted with CA(certifying authority) public key: ![image](https://github.com/himansh19/Cryptography-Algorithm/assets/89848299/4983dd7b-44d9-405a-b554-49051e67e3af)

Optional RSA Key Generation Algorithm Example: ![image](https://github.com/himansh19/Cryptography-Algorithm/assets/89848299/4f498557-8c49-4308-b50b-a94c02fda30c)


HOPE YOU LIKED THIS
     
