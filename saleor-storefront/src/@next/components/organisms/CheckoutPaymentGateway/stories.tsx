import { action } from "@storybook/addon-actions";
import { storiesOf } from "@storybook/react";
import React from "react";

import { CheckoutPaymentGateway } from ".";

const config = [{ field: "api_key", value: "pk_test_aa402cc3-c301-4183-b009-da1496fd25af" }];
const processPayment = action("processPayment");
const onError = action("onError");

storiesOf("@components/organisms/CheckoutPaymentGateway", module)
  .addParameters({ component: CheckoutPaymentGateway })
  .add("default", () => (
    <CheckoutPaymentGateway
      config={config}
      processPayment={processPayment}
      onError={onError}
    />
  ));
