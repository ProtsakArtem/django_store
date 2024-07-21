import requests
import hashlib
import hmac
import json
from random import randint
import time
from decimal import Decimal

API_URL = 'https://api.wayforpay.com/api'

class InvoiceCreateResult:
    def __init__(self, invoice_url, reason, reason_code, qr_code, order_reference):
        self.invoiceUrl = invoice_url
        self.reason = reason
        self.reasonCode = reason_code
        self.qrCode = qr_code
        self.orderReference = order_reference

    def json(self):
        return self.__dict__

class InvoiceStatusResult:
    def __init__(self, response_dict, reason, reasonCode, orderReference, amount, currency, authCode, createdDate, processingDate, cardPan, cardType, issuerBankCountry, issuerBankName, transactionStatus, refundAmount, settlementDate, settlementAmount, fee, merchantSignature):
        self.response_dict = response_dict
        self.reason = reason
        self.reasonCode = reasonCode
        self.orderReference = orderReference
        self.amount = amount
        self.currency = currency
        self.authCode = authCode
        self.createdDate = createdDate
        self.processingDate = processingDate
        self.cardPan = cardPan
        self.cardType = cardType
        self.issuerBankCountry = issuerBankCountry
        self.issuerBankName = issuerBankName
        self.transactionStatus = transactionStatus
        self.refundAmount = refundAmount
        self.settlementDate = settlementDate
        self.settlementAmount = settlementAmount
        self.fee = fee
        self.merchantSignature = merchantSignature

    def json(self):
        return self.__dict__

class WayForPay:
    def __init__(self, key, domain_name):
        self.__key = key
        self.__domain_name = domain_name

    def hash_md5(self, string):
        hash_result = hmac.new(
            self.__key.encode('utf-8'),
            string.encode('utf-8'),
            hashlib.md5
        ).hexdigest()
        print("hash:")
        print(hash_result)
        return hash_result

    def create_invoice(self, merchantAccount, merchantAuthType, amount, currency, service_url, *args, **kwargs):
        orderReference = f"DH{randint(1000000000, 9999999999)}"
        orderDate = int(time.time())

        productNames = kwargs.get('productNames', [])
        productPrices = kwargs.get('productPrices', [])
        productCounts = kwargs.get('productCounts', [])

        # Формуємо строку для підпису
        string = f'{merchantAccount};{self.__domain_name};{orderReference};{orderDate};{amount};{currency};'
        string += ';'.join(productNames) + ';'
        string += ';'.join(map(str, productCounts)) + ';'
        string += ';'.join(map(str, productPrices))
        print(string)

        params = {
            "transactionType": "CREATE_INVOICE",
            "merchantSecretKey": self.__key,
            "merchantAccount": merchantAccount,
            "merchantAuthType": merchantAuthType,
            "merchantDomainName": self.__domain_name,
            "merchantSignature": self.hash_md5(string),
            "apiVersion": "1",
            "orderReference": orderReference,
            "orderDate": orderDate,
            "amount": float(amount),  # Перетворення Decimal на float
            "currency": currency,
            "productName": productNames,
            "productPrice": [float(p) for p in productPrices],  # Перетворення Decimal на float
            "productCount": productCounts,
            'serviceUrl': service_url,
        }
        print(params['serviceUrl'])
        try:
            result = requests.post(url=API_URL, json=params)
            response_dict = json.loads(result.text)

            if result.status_code == 200 and 'invoiceUrl' in response_dict:
                invoice_url = response_dict["invoiceUrl"]
                reason = response_dict.get("reason", None)
                reason_code = response_dict.get("reasonCode", None)
                qr_code = response_dict.get("qrCode", None)
                return InvoiceCreateResult(invoice_url, reason, reason_code, qr_code, orderReference)
            else:
                print(f'Error: {response_dict}')
                if 'error' in response_dict:
                    print(f'Error detail: {response_dict["error"]}')
                return None

        except Exception as e:
            print(f'Error: {e}')
            return None

    def check_invoice(self, merchantAccount, orderReference):
        apiVersion = '1'
        string = f"{merchantAccount};{orderReference}"

        params = {
            "transactionType": "CHECK_STATUS",
            "merchantSecretKey": self.__key,
            "merchantAccount": merchantAccount,
            "orderReference": orderReference,
            "merchantSignature": self.hash_md5(string),
            "apiVersion": apiVersion
        }

        try:
            result = requests.post(url=API_URL, json=params)

            if result.status_code == 200:
                response_dict = json.loads(result.text)
                reason = response_dict["reason"]
                reasonCode = response_dict.get("reasonCode", None)
                orderReference = response_dict.get("orderReference", None)
                amount = response_dict.get("amount", None)
                currency = response_dict.get("currency", None)
                authCode = response_dict.get("authCode", None)
                createdDate = response_dict.get("createdDate", None)
                processingDate = response_dict.get("processingDate", None)
                cardPan = response_dict.get("cardPan", None)
                cardType = response_dict.get("cardType", None)
                issuerBankCountry = response_dict.get("issuerBankCountry", None)
                issuerBankName = response_dict.get("issuerBankName", None)
                transactionStatus = response_dict.get("transactionStatus", None)
                refundAmount = response_dict.get("refundAmount", None)
                settlementDate = response_dict.get("settlementDate", None)
                settlementAmount = response_dict.get("settlementAmount", None)
                fee = response_dict.get("fee", None)
                merchantSignature = response_dict.get("merchantSignature", None)

                return InvoiceStatusResult(response_dict, reason, reasonCode, orderReference, amount, currency, authCode, createdDate, processingDate, cardPan, cardType, issuerBankCountry, issuerBankName, transactionStatus, refundAmount, settlementDate, settlementAmount, fee, merchantSignature)

        except Exception as e:
            print(f'Error: {e}')
            return None

    def delete_invoice(self, merchantAccount, orderReference):
        try:
            apiVersion = '1'
            string = f"{merchantAccount};{orderReference}"
            params = {
                "transactionType": "REMOVE_INVOICE",
                "merchantSecretKey": self.__key,
                "merchantAccount": merchantAccount,
                "orderReference": orderReference,
                "merchantSignature": self.hash_md5(string),
                "apiVersion": apiVersion
            }
            result = requests.post(url=API_URL, json=params)

            if result.status_code == 200:
                return True

        except Exception as e:
            print(f'Error: {e}')
            return None
