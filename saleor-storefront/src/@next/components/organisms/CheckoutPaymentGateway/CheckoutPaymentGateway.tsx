import React, { useState } from "react";

import {ErrorMessage} from "@components/atoms";
import {CreditCardForm} from "@components/organisms";
import {IFormError} from "@types";
import {maybe, removeEmptySpaces} from "../../../../core/utils";

import * as S from "./styles";
import {
    IProps,
    ErrorData,
    ICardInputs,
    ICardPaymentInput,
    IPaymentCardError,
    PaymentData,
} from "./types";


const INITIAL_CARD_ERROR_STATE = {
    fieldErrors: {
        cvv: null,
        expirationMonth: null,
        expirationYear: null,
        number: null,
    },
    nonFieldError: "",
};

const CheckoutPaymentGateway: React.FC<IProps> = ({
                                                      config,
                                                      processPayment,
                                                      formRef,
                                                      formId,
                                                      errors = [],
                                                      postalCode,
                                                      onError,
                                                  }: IProps) => {
    const [submitErrors, setSubmitErrors] = useState<IFormError[]>([]);

    const clientToken = config.find(({field}) => field === "api_key")
        ?.value;

    const [cardErrors, setCardErrors] = React.useState<ErrorData>(
        INITIAL_CARD_ERROR_STATE
    );

    const setCardErrorsHelper = (errors: IPaymentCardError[]) =>
        errors.map(({field, message}: IPaymentCardError) =>
            setCardErrors(({fieldErrors}) => ({
                fieldErrors: {
                    ...fieldErrors,
                    [field]: {field, message},
                },
            }))
        );

    const getTokenCheckout = async (creditCard: any, clientToken: string) => {
        setCardErrors(INITIAL_CARD_ERROR_STATE);
        var myHeaders = new Headers();
        myHeaders.append("Authorization", clientToken);
        myHeaders.append("Content-Type", "application/json");


        var raw = JSON.stringify({
            "type": "card",
            "number": creditCard.number,
            "expiry_month": parseInt(creditCard.expirationDate.split("/")[0]),
            "expiry_year": parseInt(creditCard.expirationDate.split("/")[1]),
            "cvv": creditCard.cvv
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
        };

        let api_response: any = await fetch("https://api.sandbox.checkout.com/tokens", requestOptions)
            .then(response => response.text())
            .then(result => {
                return result
            })
            .catch(error => console.log('error', error));
        if (api_response) {
            api_response = JSON.parse(api_response)
            return {
                "lastDigits": api_response?.last4,
                "ccType": api_response?.product_type,
                "token": api_response?.token,
                "expMonth": api_response?.expiry_month,
                "expYear": api_response?.expiry_year,
            }
        }
        return null;
    }

    const tokenizeCcCard = async (creditCard: ICardPaymentInput) => {
        setCardErrors(INITIAL_CARD_ERROR_STATE);
        try {
            if (clientToken) {
                const cardData = (await getTokenCheckout(
                    creditCard,
                    clientToken
                )) as PaymentData;
                return cardData;
            }
            const checkoutTokenErrors = [
                {
                    message:
                        "Checkout gateway misconfigured. Client token not provided.",
                },
            ];
            setSubmitErrors(checkoutTokenErrors);
            onError(checkoutTokenErrors);
        } catch (errors) {
            setCardErrorsHelper(errors);
            onError(errors);
            return null;
        }
    };

    const handleSubmit = async (formData: ICardInputs) => {
        setSubmitErrors([]);
        const creditCard: ICardPaymentInput = {
            billingAddress: {postalCode},
            cvv: removeEmptySpaces(maybe(() => formData.ccCsc, "") || ""),
            expirationDate: removeEmptySpaces(maybe(() => formData.ccExp, "") || ""),
            number: removeEmptySpaces(maybe(() => formData.ccNumber, "") || ""),
        };
        const payment = await tokenizeCcCard(creditCard);
        if (payment?.token) {
            processPayment(payment?.token, {
                brand: payment?.ccType,
                firstDigits: null,
                lastDigits: payment?.lastDigits,
                expMonth: payment?.expMonth,
                expYear: payment?.expYear,
            });
        } else {
            const checkoutPayloadErrors = [
                {
                    message:
                        "Payment submission error. Checkout gateway returned no token in payload.",
                },
            ];
            setSubmitErrors(checkoutPayloadErrors);
            onError(checkoutPayloadErrors);
        }
    };

    const allErrors = [...errors, ...submitErrors];

    return (
        <S.Wrapper data-test="checkoutPaymentGateway">
            <CreditCardForm
                formRef={formRef}
                formId={formId}
                cardErrors={cardErrors.fieldErrors}
                labelsText={{
                    ccCsc: "CVC",
                    ccExp: "ExpiryDate",
                    ccNumber: "Number",
                }}
                disabled={false}
                handleSubmit={handleSubmit}
            />
            <ErrorMessage errors={allErrors}/>
        </S.Wrapper>
    );
};

export {CheckoutPaymentGateway};
``