# modClock - Environment Setup Guide

This guide explains how to set up the Python environment for the Raspberry Pi Zero W alarm clock project.  
Follow these steps to create the virtual environment that will be used to house dependencies and execute the project.

---

## 1. Update your Raspberry Pi

Before installing anything, make sure your system is up to date:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 2. Install required system packages

The project uses Python 3, GPIO libraries, and playsound3. Install the essentials:

```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## 3. Create the virtual environment

Inside the project folder:

```bash
python3 -m venv env
```

Activate it:

```bash
source env/bin/activate
```

You should now see `(env)` at the start of your terminal prompt.

---

## 4. Install Python dependencies

Install the dependencies from the `README.md` file.

## 5. Running the project

With the environment active:

```bash
python code.py
```

---

## 6. Deactivating the environment

When you're done working:

```bash
deactivate
```

---

## Environment successfully set up

Your Raspberry Pi modClock environment is now fully configured and reproducible.
