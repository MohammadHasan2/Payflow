import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
    console.log("Signup loaded")
  async function handleSignup() {
    await fetch("http://127.0.0.1:8000/merchants/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    nav("/");
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1>Create Account</h1>

        <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password"
          onChange={e => setPassword(e.target.value)} />

        <button onClick={handleSignup}>Sign Up</button>
      </div>
      <p>
        Already have an account?
        <button
            onClick={() => nav("/login")}
            style={{
            marginLeft: 10,
            color: "cyan",
            background: "transparent",
            border: "none",
            cursor: "pointer"
            }}
        >
            Login
        </button>
        </p>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a"
  },
  card: {
    background: "#111827",
    padding: 30,
    borderRadius: 12,
    color: "white",
    width: 300,
    display: "flex",
    flexDirection: "column",
    gap: 10
  }
};
