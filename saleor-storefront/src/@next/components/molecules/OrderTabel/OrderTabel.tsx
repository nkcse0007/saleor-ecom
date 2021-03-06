import React from "react";
import { FormattedMessage, FormattedDate, useIntl } from "react-intl";
import Media from "react-media";
import { ThemeContext } from "styled-components";

import { TaxedMoney } from "@components/containers";
import { commonMessages, translateOrderStatus } from "@temp/intl";

import { Thumbnail } from "..";
import { generateProductUrl } from "../../../../core/utils";

import * as S from "./styles";
import { IProps } from "./types";

const header = (matches: boolean) => (
  <S.HeaderRow>
    <S.IndexNumber>
      <FormattedMessage defaultMessage="Order ID " />
    </S.IndexNumber>
    {matches && (
      <>
        <S.ProductsOrdered>
          <FormattedMessage defaultMessage="Products Ordered" />
        </S.ProductsOrdered>
        <S.DateOfOrder>
          <FormattedMessage defaultMessage="Date of Order" />
        </S.DateOfOrder>
        <S.Value>
          <FormattedMessage defaultMessage="Value" />
        </S.Value>
      </>
    )}
    <S.Status>
      <FormattedMessage {...commonMessages.status} />
    </S.Status>
  </S.HeaderRow>
);

export const OrderTabel: React.FC<IProps> = ({ orders, history }: IProps) => {
  const theme = React.useContext(ThemeContext);
  const intl = useIntl();
  return (
    <S.Wrapper>
      <Media
        query={{
          minWidth: theme.breakpoints.largeScreen,
        }}
      >
        {(matches: boolean) => {
          return (
            <>
              <S.Row>{header(matches)}</S.Row>
              {orders &&
                orders.map(order => {
                  const date = new Date(order.node.created);
                  return (
                    <S.Row
                      data-test="orderEntry"
                      data-test-id={order.node.number}
                      key={order.node.number}
                      onClick={evt => {
                        evt.stopPropagation();
                        history.push(`/order-history/${order.node.token}`);
                      }}
                    >
                      <S.IndexNumber>{String(order.node.token.split("-")[0]+"0"+order.node.number).toUpperCase()}</S.IndexNumber>
                      {matches ? (
                        <>
                          <S.ProductsOrdered>
                            {order.node.lines
                              .slice(0, 5)
                              .map((product: any) => (
                                <span
                                  key={product.variant.product.id}
                                  onClick={evt => {
                                    evt.stopPropagation();
                                    history.push(
                                      generateProductUrl(
                                        product.variant.product.id,
                                        product.variant.product.name
                                      )
                                    );
                                  }}
                                >
                                  <Thumbnail source={product} />
                                </span>
                              ))}
                          </S.ProductsOrdered>
                          <S.DateOfOrder>
                            <FormattedDate value={date} />
                          </S.DateOfOrder>
                          <S.Value>
                            <TaxedMoney taxedMoney={order.node.total} />
                          </S.Value>
                        </>
                      ) : (
                        ""
                      )}
                      <S.Status>
                        {translateOrderStatus(order.node.statusDisplay, intl)}
                      </S.Status>
                    </S.Row>
                  );
                })}
            </>
          );
        }}
      </Media>
    </S.Wrapper>
  );
};
