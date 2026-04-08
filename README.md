# Warehouse Inventory Environment

A reinforcement learning environment that simulates real-world warehouse inventory management using the OpenEnv framework.

---

## 📦 Overview

This environment models a warehouse where an AI agent must manage inventory efficiently by:

- Restocking low inventory items
- Dispatching items nearing expiry
- Handling combined constraints in complex scenarios

It is designed to evaluate agent decision-making in logistics and supply chain management.

---

## 🎯 Tasks

The environment includes three tasks with increasing difficulty:

### 🟢 Easy
- Identify low-stock items
- Perform restocking actions

### 🟡 Medium
- Identify items close to expiry
- Prioritize dispatch before spoilage

### 🔴 Hard
- Handle items with:
  - Low stock
  - High demand
  - Near expiry
- Apply combined strategies (`restock_and_dispatch`)

---

## ⚙️ Action Space

Each action includes:

- `action`:
  - `restock`
  - `prioritize_dispatch`
  - `restock_and_dispatch`
- `item_name`: Target inventory item

---

## 👀 Observation Space

Each observation contains:

- `task`: Current difficulty level
- `step`: Current step number
- `items`: List of items with:
  - `item_name`
  - `stock`
  - `demand`
  - `expiry_days`

---

## 🏆 Reward Function

- ✅ +1.0 for correct action
- ⚠️ +0.3 for partially correct decisions
- ❌ 0.0 for incorrect actions

Rewards provide continuous feedback and encourage optimal decision-making.

---

## 🔄 Episode Termination

An episode ends when:

- All inventory items are in a healthy state, OR
- Maximum steps are reached

---

## 🤖 Baseline Inference

Run:

```bash
python inference.py
