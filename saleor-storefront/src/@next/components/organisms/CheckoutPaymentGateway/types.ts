import { ICardData, IFormError, IPaymentGatewayConfig } from "@types";



export interface PaymentData {
  lastDigits: string;
  ccType: string;
  token: string;
  expMonth: number;
  expYear: number;
}

export interface ICardInputs {
  ccCsc: string;
  ccExp: string;
  ccNumber: string;
}



export type CardError = { field?: string; message: string } | null;

export interface ICardPaymentInput {
  billingAddress: {
    postalCode?: string;
  };
  number: string;
  cvv: string;
  expirationDate: string;
}

export interface ICardErrors {
  cvv: CardError;
  expirationMonth: CardError;
  expirationYear: CardError;
  number: CardError;
}

export interface ErrorData {
  fieldErrors: ICardErrors;
  nonFieldError?: string;
}

export interface IPaymentCardError {
  code: string;
  field: string;
  message: string;
}


export interface IProps {
  /**
   * Payment gateway client configuration.
   */
  config: IPaymentGatewayConfig[];
  /**
   * Form reference on which payment might be submitted.
   */
  formRef?: React.RefObject<HTMLFormElement>;
  /**
   * Form id on which payment might be submitted.
   */
  formId?: string;
  /**
   * Errors returned by the payment gateway.
   */
  errors?: IFormError[];
  /**
   * Postal code used by Checkout.
   */
  postalCode?: string;
  /**
   * Method called after the form is submitted. Passed token attribute will be used to create payment.
   */
  processPayment: (token: string, cardData: ICardData) => void;
  /**
   * Method called when gateway error occured.
   */
  onError: (errors: IFormError[]) => void;
}
