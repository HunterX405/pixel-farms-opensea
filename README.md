# 🌱 Pixel Farms Marketplace Explorer

This project is a **marketplace explorer and listing viewer** for **Pixels (Pixels.xyz)**, a Web3 farming game where players can own land, customize it, and collaborate with others to farm together.

The application focuses on **discovering and browsing land plots and pets available for sale** on the **OpenSea marketplace**, helping players find assets they may want to purchase using cryptocurrency — without directly interacting with a Web3 wallet.

---

## 🧩 About Pixels

**Pixels (Pixels.xyz)** is a Web3 game built around:

* 🌾 Farming and land management
* 🗺️ NFT-based land ownership
* 🐾 Pets that provide in-game benefits
* 🤝 Cooperative gameplay on shared land

Land plots and pets are represented as NFTs and are commonly traded on marketplaces like OpenSea.

---

## 🎯 Project Focus

This project is **read-only and informational**.

It allows users to:

* 🔍 Browse **land plots** listed for sale
* 🐾 Browse **pets** that provide in-game benefits
* 🖼️ View NFT images and metadata
* 💰 See current marketplace listings and prices
* 🛒 Explore assets without connecting a wallet

⚠️ **Important:**
This project **does not**:

* Connect to a Web3 wallet
* Sign transactions
* Execute purchases

All buying actions still happen directly on OpenSea.

---

## 🧠 How It Works

* Fetches NFT listing data from the **OpenSea Marketplace API**
* Displays:

  * NFT images
  * Asset details
  * Listing prices
* Organizes assets into:

  * **Land plots**
  * **Pets**

This makes it easier for players to discover assets without manually searching the marketplace.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* OpenSea Marketplace API
* Structured data models using `dataclasses`
* Logging for debugging and traceability

No Web3 wallet libraries are used, since all interactions are read-only.

---

## 📂 Features

### 🌍 Land Explorer

* View land plots available for purchase
* See images and listing details
* Quickly scan available inventory

### 🐾 Pets Page

* Browse pets listed on OpenSea
* View pet images and metadata
* Discover pets that offer in-game advantages

---

## ▶️ Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/pixel-farms.git
cd pixel-farms
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the project

```bash
python main.py
```

---

## 📊 Logging

The project uses Python’s built-in logging system:

* **Console:** `INFO` and above
* **Log file:** `DEBUG` and above (`project.log`)

This helps with:

* Debugging API responses
* Monitoring listing fetches
* Tracing application flow

---

## ⚠️ Disclaimer

This project is **not officially affiliated with Pixels.xyz or OpenSea**.

* Pixels.xyz is a third-party Web3 game
* OpenSea is a third-party NFT marketplace
* This project is for **educational, exploratory, and tooling purposes only**

Always verify listings and prices directly on OpenSea before purchasing.

---

## 👤 Author

Created by **John Henrick Espiritu**
Focused on Python, Web3 tooling, automation, and marketplace data exploration.
