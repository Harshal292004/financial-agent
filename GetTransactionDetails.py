import requests
import json

import PaytmChecksum

paytmParams = dict()

paytmParams["body"] = {
    "mid"       : "YOUR_MID_HERE",
    "linkId"    : "31309",
}

# Generate checksum by parameters we have in body
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "YOUR_MERCHANT_KEY")

paytmParams["head"] = {
    "tokenType" : "AES",
    "signature" : checksum
}

post_data = json.dumps(paytmParams)

# for Staging
url = "https://securegw-stage.paytm.in/link/fetchTransaction"

# for Production
# url = "https://securegw.paytm.in/link/fetchTransaction"

response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
print(response)



{
    "head": {
        "version": null,
        "timestamp": "1567173128434",
        "channelId": null,
        "signature": "gywGPHQ8Tts2sqpvxtG/Tti8KP/V4RFAx+4/cZO6ohoSXMGFe/ICxryK0/igtonbp04H2uUzObemYSeMwLPA4iboX+k6GngDBrXQjuOYynU=",
        "tokenType": "AES",
        "clientId": null
    },
    "body": {
        "orders": [{
            "txnId": "20180320111212800110XXXXXXX00037880",
            "orderId": "ORDERID_98765",
            "mercUniqRef": "ORDERID_98765_12345",
            "orderCreatedTime": "2020-03-20 18:52:49",
            "orderCompletedTime": "2020-03-20 18:52:51",
            "orderType": "TRANSACTION",
            "orderStatus": "SUCCESS",
            "customerPhoneNumber": "77****7777",
            "customerEmail": "customer@example.com",
            "customerName": null,
            "txnAmount": "1.00",
            "reconId": "",
            "customerComment": "Please pack the order",
            "paymentFormData": {
                "name":"Shivam",
                "Age":"50",
                "Gender":"Male"
            }
        }],
        "merchantId": "INTEGR7769XXXXXX9383",
        "merchantName": "Test Paytm Merchant",
        "resultInfo": {
            "resultStatus": "S",
            "resultCode": "200",
            "resultMessage": "Payment link is processed successfully"
        }
    }
}    


