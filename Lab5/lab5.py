from web3.auto.infura import w3
import tqdm
import sys

K = 51
file = open('./data'+sys.argv[1]+'.csv','w')

for i in tqdm.tqdm(range(200), unit="block"):
    n = 8962400 - K*1000 + i + int(sys.argv[1])
    block = w3.eth.getBlock(n)
    gasUsed = block['gasUsed']
    gasLimit = block['gasLimit']
    miner_tax = 0
    smart_contract = 0
    transactions_count =len(block['transactions'])
    if transactions_count > 0:
        for tc in range(transactions_count):
            transaction = w3.eth.getTransactionByBlock(n,tc)
            if transaction['input'] != '0x':
                smart_contract += 1
            gasPrice = transaction['gasPrice']
            gasUsed = w3.eth.getTransactionReceipt(block['transactions'][tc])['gasUsed']
            miner_tax = miner_tax + gasUsed*gasPrice;
        text = str(w3.fromWei(miner_tax,'ether')) +","+str(transactions_count) +","+ str(smart_contract)+'\n'
        file.write(text)
file.close()
