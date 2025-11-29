# Okta Token Manager

Automate OATH Token Activation in Okta

## Overview

**Okta Token Manager** is a Python GUI application designed to simplify and automate the activation and management of **Token2 Classic OATH tokens** within Okta.
It supports **bulk CSV-based token activation**, automatic user lookup, and factor assignment—saving time and reducing manual errors for administrators.

---

## Key Features

✔ **Load CSVs containing OTP token data**
✔ **Automatically look up Okta users by email (UPN)**
✔ **Assign OATH hardware/software token factors to users**
✔ **Bulk import multiple tokens at once**
✔ **Real-time logging and progress tracking**
✔ **View Okta user details**
✔ **Test API connectivity**
✔ **Display token information and detailed error messages**

---

## Prerequisites

Before using the Okta Token Manager, ensure you have:

* An **Okta administrator account**
* An **Okta API token** with sufficient permissions (factors:read/write, users:read/write)
* **OATH tokens** ready for activation (Token2 Classic recommended)
* A **CSV file** containing token seed information

---

## Required CSV Format

Your CSV file **must** contain the following columns:

| Column Name     | Description                      | Example                                     |
| --------------- | -------------------------------- | ------------------------------------------- |
| `upn`           | User email address (Okta UPN)    | [user@company.com](mailto:user@company.com) |
| `serial number` | Token serial number              | 245252413141                                |
| `secret key`    | Token secret key                 | SN3OBMB5L7QXG5XF5WRGLFCH233655AF            |
| `timeinterval`  | Token time interval (usually 30) | 30                                          |
| `manufacturer`  | Token manufacturer               | Token2                                      |
| `model`         | Token model                      | C202                                        |

### Important Notes on CSV Preparation

* CSVs for factory-set seeds are provided by **Token2** through the seed request procedure.
  Choose the option **“CSV for Azure MFA...”** when requesting seeds.
* The CSV sent by Token2 **does not include user UPNs**, so you must manually add the `upn` column.
* **Do NOT edit the CSV in Excel.**
  Excel may corrupt the file (removing leading zeros, altering formats, etc.).
  Use a **text editor** such as Notepad instead.
* Ensure the **header row is present** exactly as shown above.

---

## How It Works

1. Load a CSV containing your prepared token list
2. The app reads each token row and attempts to match the `upn` to an Okta user
3. For each match, the app:

   * Adds an OATH token factor
   * Activates the token with the provided seed
4. Progress and errors are logged in real time

---

## Repository

**Repo name:** `okta_token_manager`

---

If you'd like, I can also add:

* Installation steps (pip, venv, dependencies)
* GUI screenshots
* Architecture diagram
* Example CSV files
  Just tell me!
