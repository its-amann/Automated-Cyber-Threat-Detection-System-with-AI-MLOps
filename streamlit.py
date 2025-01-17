import streamlit as st
import pickle
import pandas as pd
import socket
import requests
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from whois import whois


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model and preprocessor
model = pickle.load(open('final_model/model.pkl', 'rb'))
preprocessor = pickle.load(open('final_model/preprocessor.pkl', 'rb'))

# Function to make safe HTTP requests
def safe_request(url: str, timeout: int = 5) -> requests.Response:
    try:
        return requests.get(url, timeout=timeout, verify=True)
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request failed for {url}: {str(e)}")
        return None

# Feature extraction functions
def having_IP_Address(url):
    try:
        hostname = urlparse(url).hostname
        if hostname:
            socket.inet_aton(hostname)
            return 1
        return 0
    except socket.error:
        return 0

def URL_Length(url):
    return len(url)

def Shortining_Service(url):
    shortening_services = ['bit.ly', 'goo.gl', 't.co', 'tinyurl.com', 'is.gd']
    return 1 if any(service in url for service in shortening_services) else 0

def having_At_Symbol(url):
    return 1 if '@' in url else 0

def double_slash_redirecting(url):
    return 1 if url.count('//') > 2 else 0

def Prefix_Suffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

def having_Sub_Domain(url):
    return len(urlparse(url).netloc.split('.')) > 2

def SSLfinal_State(url):
    return 1 if urlparse(url).scheme == 'https' else 0

def Domain_registration_length(url):
    try:
        domain = urlparse(url).hostname
        if not domain:
            return 0
        domain_info = whois(domain)
        creation_date = domain_info.get('creation_date')
        if not creation_date:
            return 0
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (pd.to_datetime('today') - pd.to_datetime(creation_date)).days // 365
        return max(0, age)
    except Exception as e:
        logger.warning(f"Failed to get domain age for {url}: {str(e)}")
        return 0

def Favicon(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            return 1 if 'favicon.ico' in response.text else 0
        return 0
    except Exception:
        return 0

def port(url):
    return 1 if ':' in urlparse(url).netloc else 0

def HTTPS_token(url):
    return 1 if 'https' in url.lower() else 0

def Request_URL(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            imgs = soup.find_all('img', src=True)
            return 1 if any(urlparse(img['src']).netloc != urlparse(url).netloc for img in imgs) else 0
        return 0
    except Exception:
        return 0

def URL_of_Anchor(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            anchors = soup.find_all('a', href=True)
            return 1 if any(urlparse(a['href']).netloc != urlparse(url).netloc for a in anchors) else 0
        return 0
    except Exception:
        return 0

def Links_in_tags(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return len(soup.find_all(['link', 'script']))
        return 0
    except Exception:
        return 0

def SFH(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form', action=True)
            return 1 if any(not form['action'] or form['action'] == "about:blank" for form in forms) else 0
        return 0
    except Exception:
        return 0

def Submitting_to_email(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            return 1 if 'mailto:' in response.text else 0
        return 0
    except Exception:
        return 0

def Abnormal_URL(url):
    domain = urlparse(url).netloc
    return 1 if not domain or domain.startswith('http') else 0

def Redirect(url):
    try:
        response = safe_request(url)
        return 1 if len(response.history) > 1 else 0
    except Exception:
        return 0

def on_mouseover(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            return 1 if 'onmouseover=' in response.text else 0
        return 0
    except Exception:
        return 0

def RightClick(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            return 1 if 'preventdefault()' in response.text.lower() or 'event.button==2' in response.text else 0
        return 0
    except Exception:
        return 0

def popUpWindow(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            return 1 if 'window.open' in response.text else 0
        return 0
    except Exception:
        return 0

def Iframe(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            return 1 if '<iframe' in response.text or '<frame' in response.text else 0
        return 0
    except Exception:
        return 0

def age_of_domain(url):
    return Domain_registration_length(url)

def DNSRecord(url):
    try:
        domain = urlparse(url).hostname
        if domain:
            socket.gethostbyname(domain)
            return 1
        return 0
    except Exception:
        return 0

def web_traffic(url):
    try:
        response = safe_request(f"https://data.alexa.com/data?cli=10&url={url}")
        return 1 if response and response.status_code == 200 else 0
    except Exception:
        return 0

def Page_Rank(url):
    try:
        domain = urlparse(url).hostname
        response = safe_request(f"https://openpagerank.com/api/v1.0/getPageRank?domains[]={domain}")
        return 1 if response and response.status_code == 200 else 0
    except Exception:
        return 0

def Google_Index(url):
    try:
        response = safe_request(f"https://www.google.com/search?q=site:{url}")
        return 1 if response and 'did not match any documents' not in response.text else 0
    except Exception:
        return 0

def Links_pointing_to_page(url):
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return len(soup.find_all('a'))
        return 0
    except Exception:
        return 0

def Statistical_report(url):
    try:
        domain = urlparse(url).hostname
        response = safe_request(f"https://www.phishtank.com/search.php?domain={domain}")
        return 1 if response and response.status_code == 200 else 0
    except Exception:
        return 0

# Define feature extraction function based on the features provided
def extract_features(url):

    features = {
        "having_IP_Address": having_IP_Address(url),
        "URL_Length": URL_Length(url),
        "Shortining_Service": Shortining_Service(url),
        "having_At_Symbol": having_At_Symbol(url),
        "double_slash_redirecting": double_slash_redirecting(url),
        "Prefix_Suffix": Prefix_Suffix(url),
        "having_Sub_Domain": having_Sub_Domain(url),
        "SSLfinal_State": SSLfinal_State(url),
        "Domain_registeration_length": Domain_registration_length(url),
        "Favicon": Favicon(url),
        "port": port(url),
        "HTTPS_token": HTTPS_token(url),
        "Request_URL": Request_URL(url),
        "URL_of_Anchor": URL_of_Anchor(url),
        "Links_in_tags": Links_in_tags(url),
        "SFH": SFH(url),
        "Submitting_to_email": Submitting_to_email(url),
        "Abnormal_URL": Abnormal_URL(url),
        "Redirect": Redirect(url),
        "on_mouseover": on_mouseover(url),
        "RightClick": RightClick(url),
        "popUpWidnow": popUpWindow(url),
        "Iframe": Iframe(url),
        "age_of_domain": age_of_domain(url),
        "DNSRecord": DNSRecord(url),
        "web_traffic": web_traffic(url),
        "Page_Rank": Page_Rank(url),
        "Google_Index": Google_Index(url),
        "Links_pointing_to_page": Links_pointing_to_page(url),
        "Statistical_report": Statistical_report(url),
    }
    return features

# Streamlit app code
def main():
    st.title("Network Security System URL Detection App")

    st.write("This app predicts whether a URL is **Malicious**, **Suspicious** or **Safe** based on extracted features.")
    
    url = st.text_input("🔗 Enter URL:")
    analyze_button = st.button("Analyze")

    if analyze_button and url:
        with st.spinner("Analyzing URL... Please wait."):
            # Extract features
            features = extract_features(url)
            if not features:
                st.error("Error extracting features from the URL. Please try again.")
                return

            # Prepare data for prediction
            feature_df = pd.DataFrame([features])
            processed_features = preprocessor.transform(feature_df)

            # Predict using the model
            try:
                prediction = model.predict(processed_features)
                print(prediction)
                if prediction == 1:
                    st.success("The URL is **Safe**!")
                elif prediction == 0:
                    st.warning("The URL is **Suspicious**.")
                else:
                    st.error("The URL is **Malicious**!")
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
                logger.error(f"Prediction error: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()

