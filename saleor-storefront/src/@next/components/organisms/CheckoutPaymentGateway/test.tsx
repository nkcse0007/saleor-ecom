import { shallow } from "enzyme";
import "jest-styled-components";
import React from "react";

import { CheckoutPaymentGateway } from ".";

const config = [{ field: "client_token", value: "token_test_1234567890" }];

describe("<CheckoutPaymentGateway />", () => {
  it("exists", () => {
    const processPayment = jest.fn();
    const onError = jest.fn();
    const wrapper = shallow(
      <CheckoutPaymentGateway
        config={config}
        processPayment={processPayment}
        onError={onError}
      />
    );

    expect(wrapper.exists()).toEqual(true);
  });
});
