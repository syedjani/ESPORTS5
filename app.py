import os
import json
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "any-random-secret-key"

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ---- USE ENV VARIABLE ON RENDER ----
creds_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_info, scopes=SCOPE)
client = gspread.authorize(creds)

SHEET_NAME = "FF-PUBG-Slot-Bookings"
sheet = client.open(SHEET_NAME).sheet1


# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        game = request.form.get("game")
        date = request.form.get("date")
        time_slot = request.form.get("time_slot")
        ign = request.form.get("ign")  # in-game name / player ID

        # Basic validation
        if not name or not phone or not game or not date or not time_slot:
            flash("Please fill all required fields!", "error")
            return redirect(url_for("index"))

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare row data
        row = [name, phone, game, date, time_slot, ign, created_at]

        # Append to Google Sheet
        sheet.append_row(row)

        flash("Slot booked successfully! ✅", "success")
        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
