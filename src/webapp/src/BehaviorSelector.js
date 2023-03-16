import React from "react";
import Select from "react-select";

import { updateSharedState } from "./hub-state";
import st from "./BehaviorSelector.module.scss";

const options = [
  { value: 0, label: "Remote Control" },
  { value: 1, label: "Follow Pets and People" },
];

export function BehaviorSelector({ hubState }) {
  const handleChange = (option) => {
    updateSharedState({ behave: option.value });
  };
  return (
    <Select
      className={st.select}
      options={options}
      value={options[hubState.behave]}
      isSearchable={false}
      isClearable={false}
      onChange={handleChange}
      classNamePrefix="react-select"
    />
  );
}
