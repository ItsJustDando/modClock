# modClock - Environment Setup Guide

This guide explains how to set up the Python environment for the Raspberry Pi Zero W alarm clock project.  
Follow these steps to recreate the development environment from scratch.

---

## 1. Update your Raspberry Pi

Before installing anything, make sure your system is up to date:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 2. Install required system packages

The project uses Python 3, GPIO libraries, and audio playback tools. Install the essentials:

```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## 3. Clone the repository

If you haven’t already:

```bash
git clone https://github.com/ItsJustDando/modClock.git
cd modClock
```

---

## 4. Create the virtual environment

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

## 5. Install Python dependencies

The repo includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If it does not work, install the dependencies from the `README.md` file

## 6. Running the project

With the environment active:

```bash
python code.py
```

(Replace `main.py` with your actual entry point.)

---

## 8. Deactivating the environment

When you're done working:

```bash
deactivate
```

---

## Environment successfully set up

Your Raspberry Pi alarm clock environment is now fully configured and reproducible.
