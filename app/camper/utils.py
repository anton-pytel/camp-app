# -*- coding: utf-8 -*-
import string
import random
import requests
import json
import smtplib
from datetime import datetime
from email.message import EmailMessage
from unidecode import unidecode

# characters to generate password from
characters = list(string.ascii_letters + string.digits + "!")


def filter_f_l_name(objects, f_name, l_name):
    result = []
    for obj in objects:
        if unidecode(obj.user.first_name.lower()) == unidecode(f_name.lower()) and \
                unidecode(obj.user.last_name.lower()) == unidecode(l_name.lower()):
            result.append(obj)
    return result



def generate_random_password(length):
    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(password)

    # converting the list to string
    return "".join(password)


def get_username(p_name, l_name, sfx):
    return f"{unidecode(p_name.lower())}.{unidecode(l_name.lower())}-{sfx}"


def get_qr(iban, amount, due_date, vs='', ks='', ss='', msg=''):
    url = "https://bsqr.co/generator/qr.php"
    iban = iban.replace(' ', '')
    msg = msg[:140]
    if type(due_date) == datetime:
        due_date = due_date.strftime("%Y-%m-%d")
    # due date not used any more
    payload = f'bank_account_format=IBAN&Pay%5BPayments%5D%5BPayment%5D%5BBankAccounts%5D%5BBankAccount%5D%5BIBAN%5D={iban}&Pay%5BPayments%5D%5BPayment%5D%5BBankAccounts%5D%5BBankAccount%5D%5BBIC%5D=&Pay%5BPayments%5D%5BPayment%5D%5BVariableSymbol%5D={vs}&Pay%5BPayments%5D%5BPayment%5D%5BConstantSymbol%5D={ks}&Pay%5BPayments%5D%5BPayment%5D%5BSpecificSymbol%5D={ss}&Pay%5BPayments%5D%5BPayment%5D%5BBeneficiaryAddressLine1%5D=&Pay%5BPayments%5D%5BPayment%5D%5BBeneficiaryAddressLine2%5D=&Pay%5BPayments%5D%5BPayment%5D%5BAmount%5D={amount}&Pay%5BPayments%5D%5BPayment%5D%5BCurrencyCode%5D=EUR&Pay%5BPayments%5D%5BPayment%5D%5BPaymentDueDate%5D=&Pay%5BPayments%5D%5BPayment%5D%5BOriginatorsReferenceInformation%5D=&Pay%5BPayments%5D%5BPayment%5D%5BPaymentNote%5D={msg}&Pay%5BPayments%5D%5BPayment%5D%5BBeneficiaryName%5D=&Invoice%5BInvoiceID%5D=2015001&Invoice%5BIssueDate%5D=2021-12-31&Invoice%5BTaxPointDate%5D=2021-12-31&Invoice%5BOrderID%5D=&Invoice%5BDeliveryNoteID%5D=&Invoice%5BLocalCurrencyCode%5D=EUR&Invoice%5BSupplierParty%5D%5BPartyName%5D=ADELANTE%2C%20s.r.o.&Invoice%5BSupplierParty%5D%5BCompanyTaxID%5D=2021802651&Invoice%5BSupplierParty%5D%5BCompanyVATID%5D=SK2021802651&Invoice%5BSupplierParty%5D%5BCompanyRegisterID%5D=36557561&Invoice%5BSupplierParty%5D%5BContact%5D%5BName%5D=&Invoice%5BSupplierParty%5D%5BContact%5D%5BTelephone%5D=&Invoice%5BSupplierParty%5D%5BContact%5D%5BEMail%5D=&Invoice%5BSupplierParty%5D%5BPostalAddress%5D%5BStreetName%5D=%C5%A0pit%C3%A1lska&Invoice%5BSupplierParty%5D%5BPostalAddress%5D%5BBuildingNumber%5D=10&Invoice%5BSupplierParty%5D%5BPostalAddress%5D%5BCityName%5D=Bratislava&Invoice%5BSupplierParty%5D%5BPostalAddress%5D%5BPostalZone%5D=811%2008&Invoice%5BSupplierParty%5D%5BPostalAddress%5D%5BState%5D=&Invoice%5BSupplierParty%5D%5BPostalAddress%5D%5BCountry%5D=SVK&Invoice%5BCustomerParty%5D%5BPartyName%5D=iLancer%20s.r.o.&Invoice%5BCustomerParty%5D%5BCompanyTaxID%5D=2023187133&Invoice%5BCustomerParty%5D%5BCompanyVATID%5D=SK2023187133&Invoice%5BCustomerParty%5D%5BCompanyRegisterID%5D=45960119&Invoice%5BCustomerParty%5D%5BPartyIdentification%5D=&3=header&Invoice%5BInvoiceDescription%5D=Fakturujeme%20V%C3%A1m%20za%20dodan%C3%BD%20tovar%20a%20slu%C5%BEby&Invoice%5BTaxCategorySummaries%5D%5BTaxCategorySummary_0%5D%5BClassifiedTaxCategory%5D=20&Invoice%5BTaxCategorySummaries%5D%5BTaxCategorySummary_0%5D%5BTaxExclusiveAmount%5D=1000&Invoice%5BTaxCategorySummaries%5D%5BTaxCategorySummary_0%5D%5BTaxAmount%5D=200.00&Invoice%5BTaxCategorySummaries%5D%5BTaxCategorySummary_0%5D%5BAlreadyClaimedTaxExclusiveAmount%5D=0&Invoice%5BTaxCategorySummaries%5D%5BTaxCategorySummary_0%5D%5BAlreadyClaimedTaxAmount%5D=0.00&Invoice%5BMonetarySummary%5D%5BPayableRoundingAmount%5D=0&Invoice%5BMonetarySummary%5D%5BPaidDepositsAmount%5D=0&Invoice%5BPaymentMeans%5D%5B%5D=moneyTransfer'
    headers = {
        'referer': 'https://bsqr.co/generator/?from=bysquare_main_menu',
        'origin': 'https://bsqr.co',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    res = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    if res.status_code == 200:
        pay_obj = json.loads(res.content)
        if 'Pay' in pay_obj:
            qr = pay_obj['Pay']['src']
            return qr
    return ''


def send_mail(server_config: dict, subject: str, text: str, mail_from: str, mail_to: list):
    """
    :param server_config: { 'host': '10.0.0.1', 'port': 587
                            'username': 'user', 'password: 'pass'
                          }
    :param subject: mail subject
    :param text: mail message
    :param mail_from: sender
    :param mail_to: recepients (array expected
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = ', '.join(mail_to)
    msg.add_alternative(text, subtype='html')
    sc = server_config

    s = smtplib.SMTP(host=sc['host'], port=sc['port'])
    s.starttls()
    s.ehlo()
    s.login(sc['username'], sc['password'])
    s.send_message(msg, to_addrs=mail_to)
    s.quit()
