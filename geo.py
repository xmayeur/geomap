import logging
import sys
from time import sleep

import folium
import pandas as pd
from geopy.geocoders import TomTom
from getSecrets import get_secret


def init_log(log_file=None):
    """
    Initialize the logging module to the sdterr output and to the log file
    :param log_file: the log file path
    :return: a logger object
    """
    # if os.path.exists("sendMail.log"):
    #     os.remove("sendMail.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


log = init_log(log_file="geomap.log")

key = get_secret("TomTomAPI")["key"]

# geolocator = Nominatim(user_agent="my_geocoder")
geolocator = TomTom(api_key=key)
addresses_file = "/Users/xavier/PycharmProjects/geomap/liste.csv"

location = geolocator.geocode("Bruxelles, Belgique")
m = folium.Map([location.latitude, location.longitude], zoom_start=9)

L.tileLayer.provider('TomTom', {
    "apikey": key
}).addTo(map);

df = pd.read_csv(addresses_file)
for idx, r in df.iterrows():
    sleep(1)
    if idx > 1000:
        break
    if not r["cotisationExpiration"]:
        continue
    country = {
        "BE": "Belgique"
    }
    address = ""
    try:
        pays = country[r["adressePays"]].strip()
        if not pays:
            pays = "Belgique"
        address = str(r["adresseNumero"]) + " " + r["adresseRue"].strip() + ", " + str(int(r["adresseCp"])) + " " + r[
            "adresseVille"].strip() + ", " + pays

        location = geolocator.geocode(address)
        # print(location)
        folium.Marker(
            location=[location.latitude, location.longitude],
            tooltip=r["prenom"] + " " + r["nom"],
            popup=address,
            icon=folium.Icon(color="red"),
        ).add_to(m)
    except:
        log.error("X " + r["prenom"] + " " + r["nom"] + " " + address)
        continue
    log.info(r["prenom"] + " " + r["nom"])
m.save("/Users/xavier/PycharmProjects/geomap/index.html")
