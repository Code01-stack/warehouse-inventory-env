---
title: Warehouse Inventory Env
emoji: 📦
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# 📦 Warehouse Inventory Environment

A **real-world reinforcement learning environment** for optimizing warehouse inventory operations.  
This environment simulates decision-making tasks such as restocking, dispatching, and managing expiring goods.

---

## 🎯 Motivation

Warehouse management is a critical real-world problem involving:

- Inventory optimization  
- Demand fulfillment  
- Waste reduction due to expiry  

This environment enables evaluation of agent reasoning in **logistics and supply chain scenarios**.

---

## 🧠 Tasks (Difficulty Levels)

### 🟢 Easy — Restocking
- Objective: Identify low-stock items and restock them  
- Reward:  
  - ✅ Correct restock → 1.0  
  - ⚠️ Partial progress → 0.3  

---

### 🟡 Medium — Expiry Handling
- Objective: Prioritize dispatch of items nearing expiry  
- Reward:  
  - ✅ Correct dispatch → 1.0  
  - ⚠️ Partial signal → 0.3  

---

### 🔴 Hard — Combined Optimization
- Objective: Handle:
  - Low stock  
  - High demand  
  - Expiring items  
- Reward:
  - ✅ Optimal action → 1.0  
  - ⚠️ Partial progress → 0.3  

---

## ⚙️ Action Space

```json
{
  "action": "restock | prioritize_dispatch | restock_and_dispatch",
  "item_name": "string"
}