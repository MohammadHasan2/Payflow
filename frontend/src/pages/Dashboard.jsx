import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const nav = useNavigate();

  const apiKey = localStorage.getItem("apiKey");
  const token = localStorage.getItem("token");

  const [amount, setAmount] = useState("");

  async function createPayment() {
    const res = await fetch(
      `http://127.0.0.1:8000/create-payment?amount=${amount}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Idempotency-Key": crypto.randomUUID()
        }
      }
    );

    const data = await res.json();
    window.location.href = data.checkout_url;
  }

  function logout() {
    localStorage.clear();
    nav("/");
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1>Dashboard</h1>

        <h3>Your API Key</h3>
        <code style={styles.box}>{apiKey}</code>

        <h3>Create Payment</h3>

        <input
          placeholder="Amount"
          onChange={e => setAmount(e.target.value)}
        />

        <button onClick={createPayment}>
          Pay
        </button>

        <button onClick={logout} style={{ background: "red" }}>
          Logout
        </button>
      </div>
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
    width: 400,
    display: "flex",
    flexDirection: "column",
    gap: 10
  },
  box: {
    background: "#1f2937",
    padding: 10,
    borderRadius: 6,
    wordBreak: "break-all"
  }
};