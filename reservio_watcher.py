"""
Reservio Availability Watcher — Version finale
================================================
Surveille https://dominiquedujardin.reservio.com/order?what=time
et envoie un email + alerte sonore dès qu'un créneau se libère.

INSTALLATION (une seule fois, dans un terminal) :
    pip install playwright
    playwright install chromium

LANCEMENT :
    python reservio_watcher.py

Appuie sur Ctrl+C pour arrêter.
"""

import time
import smtplib
import winsound
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from playwright.sync_api import sync_playwright

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

URL = "https://dominiquedujardin.reservio.com/order?what=time"

# Intervalle entre chaque vérification (secondes)
CHECK_INTERVAL = 60  # 1 minute

# Email
GMAIL_ADDRESS  = "houssemrezgui69@gmail.com"
GMAIL_APP_PWD  = "lscphlquqzjystap"   # mot de passe d'application (sans espaces)
EMAIL_DEST     = "houssemrezgui69@gmail.com"

# Sélecteur CSS exact du message "Aucun créneau disponible" (trouvé via DevTools)
NO_SLOT_SELECTOR = "span.styles-module__PVNKyW__root"
NO_SLOT_TEXT     = "aucun créneau disponible"

# ──────────────────────────────────────────────────────────────────────────────


def log(msg: str):
    ts = datetime.now().strftime("%d/%m %H:%M:%S")
    print(f"[{ts}] {msg}")


def play_alert():
    """3 bips d'alerte Windows."""
    for _ in range(3):
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        time.sleep(0.4)


def send_email():
    """Envoie un email de notification via Gmail SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🟢 Créneau disponible sur Reservio !"
        msg["From"]    = GMAIL_ADDRESS
        msg["To"]      = EMAIL_DEST

        html = f"""
        <html><body style="font-family:Arial,sans-serif;padding:20px;">
            <h2 style="color:#2e7d32;">Un creneau vient de se liberer !</h2>
            <p>Le site <strong>Dominique Dujardin / Reservio</strong> affiche
            maintenant des creneaux disponibles.</p>
            <p style="margin:20px 0;">
                <a href="{URL}"
                   style="background:#1976d2;color:#fff;padding:12px 24px;
                          text-decoration:none;border-radius:6px;font-size:16px;">
                    Reserver maintenant
                </a>
            </p>
            <p style="color:#888;font-size:12px;">
                Detecte le {datetime.now().strftime("%d/%m/%Y a %H:%M:%S")}
            </p>
        </body></html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PWD)
            server.sendmail(GMAIL_ADDRESS, EMAIL_DEST, msg.as_string())

        log("Email envoye avec succes !")
    except Exception as e:
        log(f"Erreur envoi email : {e}")


def check_availability(page) -> bool:
    page.goto(URL, wait_until="domcontentloaded", timeout=30_000)
    time.sleep(5)

    # Attendre que le texte apparaisse (max 15s)
    try:
        page.wait_for_selector(f"text={NO_SLOT_TEXT}", timeout=15_000)
        return False  # "Aucun créneau disponible" trouvé
    except:
        # Si le texte n'apparaît pas → vérifier s’il y a VRAIMENT des slots
        pass

    # Vérification secondaire : présence d’éléments cliquables (créneaux)
    # Cherche des éléments typiques de créneaux (texte horaire)
    time_slots = page.query_selector_all("text=:")

    # Exemple : "09:00", "14:30", etc.
    valid_slots = []
    for el in time_slots:
        txt = el.inner_text().strip()
        if ":" in txt and len(txt) <= 5:
            valid_slots.append(txt)

    if len(valid_slots) > 0:
        return True

    return False

def main():
    log("=" * 55)
    log(" Reservio Watcher - demarrage")
    log(f" URL      : {URL}")
    log(f" Email    : {EMAIL_DEST}")
    log(f" Intervalle : {CHECK_INTERVAL}s")
    log("=" * 55)
    log("Appuie sur Ctrl+C pour arreter.\n")

    attempt       = 0
    last_notified = None   # evite de spammer si la dispo dure plusieurs checks

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        try:
            while True:
                attempt += 1
                log(f"Verification #{attempt}...")

                try:
                    dispo = check_availability(page)
                except Exception as e:
                    log(f"Erreur chargement : {e}")
                    dispo = False

                if dispo:
                    log("DISPONIBILITE TROUVEE !")
                    play_alert()

                    # N'envoie l'email qu'une fois par heure max
                    now = datetime.now()
                    if last_notified is None or (now - last_notified).seconds > 3600:
                        send_email()
                        last_notified = now
                    else:
                        log("(Email deja envoye recemment, pas de doublon)")

                else:
                    log("Aucun creneau pour l'instant.")

                log(f"Prochain check dans {CHECK_INTERVAL}s...\n")
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log("\nArret demande. A bientot !")
        finally:
            browser.close()


if __name__ == "__main__":
    main()