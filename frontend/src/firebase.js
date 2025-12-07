// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDgXdO0q3PQKUO_Y4aQ-nHrGl7ISKs5B58",
  authDomain: "quickquiz-375.firebaseapp.com",
  projectId: "quickquiz-375",
  storageBucket: "quickquiz-375.firebasestorage.app",
  messagingSenderId: "354151537917",
  appId: "1:354151537917:web:ee38613bc6045e8c09f294"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();

export const loginWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    const token = await result.user.getIdToken();
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify({
      name: result.user.displayName,
      email: result.user.email,
      photoURL: result.user.photoURL
    }));
    return result.user;
  } catch (err) {
    console.error("Google Sign-In Error:", err);
  }
};

export const logout = async () => {
  await signOut(auth);
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};
