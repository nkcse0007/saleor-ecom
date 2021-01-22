from decimal import Decimal
from typing import Dict
import checkout_sdk as sdk

from django_countries import countries

# List of zero-decimal currencies
# Since there is no public API in Checkout backend or helper function
# in Checkout's Python library, this list is straight out of Checkout's docs
# https://Checkout.com/docs/currencies#zero-decimal
from ...interface import AddressData, PaymentData

ZERO_DECIMAL_CURRENCIES = [
    "BIF",
    "CLP",
    "DJF",
    "GNF",
    "JPY",
    "KMF",
    "KRW",
    "MGA",
    "PYG",
    "RWF",
    "UGX",
    "VND",
    "VUV",
    "XAF",
    "XOF",
    "XPF",
]

CURRENCIES_CHOICE={
    "ALL" : sdk.Currency.ALL,
    "STN" : sdk.Currency.STN,
    "EEK" : sdk.Currency.EEK,
    "BHD" : sdk.Currency.BHD,
    "SCR" : sdk.Currency.SCR,
    "DJF" : sdk.Currency.DJF,
    "EGP" : sdk.Currency.EGP,
    "MDL" : sdk.Currency.MDL,
    "MZN" : sdk.Currency.MZN,
    "BND" : sdk.Currency.BND,
    "ZMK" : sdk.Currency.ZMK,
    "SHP" : sdk.Currency.SHP,
    "LBP" : sdk.Currency.LBP,
    "AWG" : sdk.Currency.AWG,
    "JMD" : sdk.Currency.JMD,
    "KES" : sdk.Currency.KES,
    "BYN" : sdk.Currency.BYN,
    "KHR" : sdk.Currency.KHR,
    "LAK" : sdk.Currency.LAK,
    "MVR" : sdk.Currency.MVR,
    "AOA" : sdk.Currency.AOA,
    "TJS" : sdk.Currency.TJS,
    "SVC" : sdk.Currency.SVC,
    "GNF" : sdk.Currency.GNF,
    "BRL" : sdk.Currency.BRL,
    "MOP" : sdk.Currency.MOP,
    "BOB" : sdk.Currency.BOB,
    "CDF" : sdk.Currency.CDF,
    "NAD" : sdk.Currency.NAD,
    "LYD" : sdk.Currency.LYD,
    "VUV" : sdk.Currency.VUV,
    "QAR" : sdk.Currency.QAR,
    "CLP" : sdk.Currency.CLP,
    "HRK" : sdk.Currency.HRK,
    "ISK" : sdk.Currency.ISK,
    "FKP" : sdk.Currency.FKP,
    "XCD" : sdk.Currency.XCD,
    "NOK" : sdk.Currency.NOK,
    "CUP" : sdk.Currency.CUP,
    "VND" : sdk.Currency.VND,
    "PEN" : sdk.Currency.PEN,
    "KMF" : sdk.Currency.KMF,
    "LVL" : sdk.Currency.LVL,
    "MMK" : sdk.Currency.MMK,
    "TRY" : sdk.Currency.TRY,
    "VEF" : sdk.Currency.VEF,
    "AUD" : sdk.Currency.AUD,
    "TWD" : sdk.Currency.TWD,
    "PKR" : sdk.Currency.PKR,
    "SLL" : sdk.Currency.SLL,
    "BGN" : sdk.Currency.BGN,
    "LRD" : sdk.Currency.LRD,
    "LKR" : sdk.Currency.LKR,
    "XAF" : sdk.Currency.XAF,
    "JOD" : sdk.Currency.JOD,
    "ANG" : sdk.Currency.ANG,
    "BSD" : sdk.Currency.BSD,
    "CAD" : sdk.Currency.CAD,
    "GIP" : sdk.Currency.GIP,
    "MNT" : sdk.Currency.MNT,
    "LTL" : sdk.Currency.LTL,
    "BBD" : sdk.Currency.BBD,
    "CLF" : sdk.Currency.CLF,
    "BWP" : sdk.Currency.BWP,
    "COP" : sdk.Currency.COP,
    "PHP" : sdk.Currency.PHP,
    "HUF" : sdk.Currency.HUF,
    "FJD" : sdk.Currency.FJD,
    "MWK" : sdk.Currency.MWK,
    "THB" : sdk.Currency.THB,
    "XPF" : sdk.Currency.XPF,
    "RSD" : sdk.Currency.RSD,
    "SAR" : sdk.Currency.SAR,
    "UYU" : sdk.Currency.UYU,
    "BZD" : sdk.Currency.BZD,
    "SYP" : sdk.Currency.SYP,
    "GMD" : sdk.Currency.GMD,
    "SZL" : sdk.Currency.SZL,
    "SBD" : sdk.Currency.SBD,
    "ETB" : sdk.Currency.ETB,
    "CHF" : sdk.Currency.CHF,
    "MXN" : sdk.Currency.MXN,
    "ARS" : sdk.Currency.ARS,
    "GTQ" : sdk.Currency.GTQ,
    "GHS" : sdk.Currency.GHS,
    "NIO" : sdk.Currency.NIO,
    "JPY" : sdk.Currency.JPY,
    "BDT" : sdk.Currency.BDT,
    "UZS" : sdk.Currency.UZS,
    "SOS" : sdk.Currency.SOS,
    "BTN" : sdk.Currency.BTN,
    "NZD" : sdk.Currency.NZD,
    "TZS" : sdk.Currency.TZS,
    "IQD" : sdk.Currency.IQD,
    "MGA" : sdk.Currency.MGA,
    "DZD" : sdk.Currency.DZD,
    "GYD" : sdk.Currency.GYD,
    "USD" : sdk.Currency.USD,
    "KWD" : sdk.Currency.KWD,
    "CNY" : sdk.Currency.CNY,
    "PYG" : sdk.Currency.PYG,
    "SGD" : sdk.Currency.SGD,
    "KZT" : sdk.Currency.KZT,
    "PGK" : sdk.Currency.PGK,
    "AMD" : sdk.Currency.AMD,
    "GBP" : sdk.Currency.GBP,
    "AFN" : sdk.Currency.AFN,
    "CRC" : sdk.Currency.CRC,
    "XOF" : sdk.Currency.XOF,
    "YER" : sdk.Currency.YER,
    "MRU" : sdk.Currency.MRU,
    "DKK" : sdk.Currency.DKK,
    "TOP" : sdk.Currency.TOP,
    "INR" : sdk.Currency.INR,
    "SDG" : sdk.Currency.SDG,
    "DOP" : sdk.Currency.DOP,
    "ZWL" : sdk.Currency.ZWL,
    "UGX" : sdk.Currency.UGX,
    "SEK" : sdk.Currency.SEK,
    "LSL" : sdk.Currency.LSL,
    "MYR" : sdk.Currency.MYR,
    "TMT" : sdk.Currency.TMT,
    "OMR" : sdk.Currency.OMR,
    "BMD" : sdk.Currency.BMD,
    "KRW" : sdk.Currency.KRW,
    "HKD" : sdk.Currency.HKD,
    "KGS" : sdk.Currency.KGS,
    "BAM" : sdk.Currency.BAM,
    "NGN" : sdk.Currency.NGN,
    "ILS" : sdk.Currency.ILS,
    "MUR" : sdk.Currency.MUR,
    "RON" : sdk.Currency.RON,
    "TND" : sdk.Currency.TND,
    "AED" : sdk.Currency.AED,
    "PAB" : sdk.Currency.PAB,
    "NPR" : sdk.Currency.NPR,
    "TTD" : sdk.Currency.TTD,
    "RWF" : sdk.Currency.RWF,
    "HTG" : sdk.Currency.HTG,
    "IDR" : sdk.Currency.IDR,
    "EUR" : sdk.Currency.EUR,
    "KYD" : sdk.Currency.KYD,
    "IRR" : sdk.Currency.IRR,
    "KPW" : sdk.Currency.KPW,
    "MKD" : sdk.Currency.MKD,
    "SRD" : sdk.Currency.SRD,
    "HNL" : sdk.Currency.HNL,
    "AZN" : sdk.Currency.AZN,
    "ERN" : sdk.Currency.ERN,
    "CZK" : sdk.Currency.CZK,
    "CVE" : sdk.Currency.CVE,
    "BIF" : sdk.Currency.BIF,
    "MAD" : sdk.Currency.MAD,
    "RUB" : sdk.Currency.RUB,
    "UAH" : sdk.Currency.UAH,
    "WST" : sdk.Currency.WST,
    "PLN" : sdk.Currency.PLN,
    "ZAR" : sdk.Currency.ZAR,
    "GEL" : sdk.Currency.GEL,
    "ZMW" : sdk.Currency.ZMW,
}


def get_amount_for_checkout(amount, currency):
    """Get appropriate amount for Checkout.

    Checkout is using currency's smallest unit such as cents for USD and
    Checkout requires integer instead of decimal, so multiplying by 100
    and converting to integer is required. But for zero-decimal currencies,
    multiplying by 100 is not needed.
    """
    # Multiply by 100 for non-zero-decimal currencies
    if currency.upper() not in ZERO_DECIMAL_CURRENCIES:
        amount *= 100

    # Using int(Decimal) directly may yield wrong result
    # such as int(Decimal(24.24)*100) will equal to 2423
    return int(amount.to_integral_value())


def get_amount_from_checkout(amount, currency):
    """Get appropriate amount from Checkout."""
    amount = Decimal(amount)

    # Divide by 100 for non-zero-decimal currencies
    if currency.upper() not in ZERO_DECIMAL_CURRENCIES:
        # Using Decimal(amount / 100.0) will convert to decimal from float
        # where precision may be lost
        amount /= Decimal(100)

    return amount


def get_currency_for_checkout(currency):
    """Convert Saleor's currency format to Checkout's currency format.

    Checkout's currency is using lowercase while Saleor is using uppercase.
    """
    print(currency)
    return CURRENCIES_CHOICE[currency.upper()] if CURRENCIES_CHOICE[currency.upper()] else None


def get_currency_from_checkout(currency):
    """Convert Checkout's currency format to Saleor's currency format.

    Checkout's currency is using lowercase while Saleor is using uppercase.
    """
    return currency.upper()


def get_payment_billing_fullname(payment_information: PaymentData) -> str:
    # Get billing name from payment
    payment_billing = payment_information.billing
    if not payment_billing:
        return ""
    return "%s %s" % (payment_billing.last_name, payment_billing.first_name)


def shipping_to_checkout_dict(shipping: AddressData) -> Dict:
    return {
        "address":
            {
                "address_line1": shipping.street_address_1,
                "address_line2": shipping.street_address_2,
                "city": shipping.city,
                "state": shipping.country_area,
                "zip": shipping.postal_code,
                "country": shipping.country
            }
    }
