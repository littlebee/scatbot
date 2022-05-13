import React from "react";

import { classnames } from "../util/classNames";
import st from "./Button.module.css";

export function Button({ className, children, isSelected, onClick }) {
  const buttonCls = classnames(className, "button", st.button, {
    predicate: isSelected,
    value: st.buttonSelected,
  });
  return (
    <div className={buttonCls} onClick={onClick}>
      <a>{children}</a>
    </div>
  );
}
