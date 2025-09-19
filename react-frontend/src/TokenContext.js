import React, { createContext, useState, useContext } from "react";

const TokenContext = createContext();

export function TokenProvider({ children }) {
  const [idToken, setIdToken] = useState(null);
  return (
    <TokenContext.Provider value={{ idToken, setIdToken }}>
      {children}
    </TokenContext.Provider>
  );
}

export function useToken() {
  return useContext(TokenContext);
}
