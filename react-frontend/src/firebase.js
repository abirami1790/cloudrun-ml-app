import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAzMWuq10fkTFaaVpfLptBNphIIcdM01dA",
  authDomain: "dsights-golden-test-99.firebaseapp.com",
  projectId: "dsights-golden-test-99"
  
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
