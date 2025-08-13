#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
import os

# ===== Colors =====
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ===== Banner =====
BANNER = f"""
{CYAN}

██████╗ ██╗     ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗     
██╔══██╗██║     ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗    
██████╔╝██║     █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝    
██╔══██╗██║     ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    
██████╔╝███████╗██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║    
╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝    
                                                                 
{RED}               BLFinder — Made by MR BINU
{RESET}
"""

# ===== Globals =====
HEADERS = {'User-Agent': 'Mozilla/5.0'}
visited = set()
broken_links = dict()
RESULT_DIR = "BLFinder_results"
BROKEN_CODES = [404]  # Sirf 404 ko broken maan lo

# ===== Helpers =====
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def normalize_url(url):
    parsed = urlparse(url)
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    return clean_url.rstrip('/')

def is_external(base_url, link):
    return urlparse(base_url).netloc != urlparse(link).netloc

def check_link_status(url):
    try:
        resp = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        if resp.status_code in [403, 405, 400, 0]:
            resp = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True, stream=True)
        return resp.status_code
    except Exception:
        return None

# ===== Crawler =====
def crawl(url, base_url, depth=2, verbose=True):
    norm_url = normalize_url(url)
    if depth == 0 or norm_url in visited:
        return
    visited.add(norm_url)

    if verbose:
        print(f"{CYAN}🔍 Crawling: {url}{RESET}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        for link in links:
            full_url = urljoin(url, link)
            if not is_valid_url(full_url):
                continue

            full_url = normalize_url(full_url)

            if is_external(base_url, full_url):
                status = check_link_status(full_url)
                if status is not None and status in BROKEN_CODES:
                    print(f"{RED}[❌] Broken External: {full_url} (Status: {status}){RESET}")
                    if url not in broken_links:
                        broken_links[url] = []
                    broken_links[url].append(full_url)
                elif verbose:
                    print(f"{GREEN}[✅] OK External: {full_url} (Status: {status}){RESET}")
            else:
                crawl(full_url, base_url, depth - 1, verbose)

    except Exception as e:
        if verbose:
            print(f"{YELLOW}⚠️ Error crawling {url} -> {e}{RESET}")

# ===== Input Handler =====
def show_creator_info():
    creator_banner = f"""
{CYAN}
╔════════════════════════════════════════════════════════╗
║                   ABOUT CREATOR                       ║
╚════════════════════════════════════════════════════════╝
{YELLOW}You want to know about me? See my social media profiles!{RESET}
{GREEN}
Instagram : https://www.instagram.com/__mr.binu__
Twitter   : https://x.com/MR_BINU_BB
GitHub    : https://github.com/MR-BINU-BB
Linkedin  : https://www.linkedin.com/in/mr-binu-416b16374
YouTube   : Soon
{RESET}
"""
    print(creator_banner)
    print(f"{YELLOW}1.{RESET} Main Menu")
    print(f"{YELLOW}2.{RESET} Exit")
    choice = input(f"{CYAN}Select option: {RESET}").strip()
    if choice == "1":
        return True  # Go back to main menu
    elif choice == "2":
        print(f"{RED}Exiting tool...{RESET}")
        exit()
    else:
        print(f"{RED}Invalid choice.{RESET}")
        exit()

# ===== Target input =====
def get_targets():
    while True:
        print(f"{YELLOW}1.{RESET} Single site")
        print(f"{YELLOW}2.{RESET} Sites list file")
        print(f"{YELLOW}3.{RESET} About Creator")
        print(f"{YELLOW}4.{RESET} Exit")
        choice = input(f"{CYAN}Select option: {RESET}").strip()
        if choice == "1":
            site = input("Enter site URL: ").strip()
            # Result file name input
            while True:
                result_name = input(f"{CYAN}Enter result file name (without .txt): {RESET}").strip()
                result_path = os.path.join(RESULT_DIR, f"{result_name}.txt")
                if os.path.exists(result_path):
                    print(f"{RED}File '{result_name}.txt' already exists! Please enter a new name.{RESET}")
                else:
                    break
            return [site if site.startswith("http") else "http://" + site], result_path
        elif choice == "2":
            path = input("Enter file path: ").strip()
            while True:
                result_name = input(f"{CYAN}Enter result file name (without .txt): {RESET}").strip()
                result_path = os.path.join(RESULT_DIR, f"{result_name}.txt")
                if os.path.exists(result_path):
                    print(f"{RED}File '{result_name}.txt' already exists! Please enter a new name.{RESET}")
                else:
                    break
            with open(path, "r", encoding="utf-8") as f:
                sites = [(line.strip() if line.startswith("http") else "http://" + line.strip()) for line in f if line.strip()]
            return sites, result_path
        elif choice == "3":
            if show_creator_info():
                print(BANNER)
                continue
        elif choice == "4":
            print(f"{RED}Exiting tool...{RESET}")
            exit()
        else:
            print(f"{RED}Invalid choice.{RESET}")
            exit()
# ===== Main =====
if __name__ == "__main__":
    print(BANNER)
    ensure_dir(RESULT_DIR)
    try:
        targets, result_path = get_targets()
        depth = int(input(f"{CYAN}Enter crawl depth (e.g., 2 for normal, 5+ for deep): {RESET}"))
        verbose_mode = input("Enable verbose mode? (y/n): ").strip().lower() == "y"

        for target in targets:
            crawl(target, target, depth=depth, verbose=verbose_mode)

    except KeyboardInterrupt:
        print(f"\n{RED}Scan interrupted by user! Saving results...{RESET}")

    # Save results
    with open(result_path, "w", encoding="utf-8") as f:
        for source, links in broken_links.items():
            f.write(f"Source: {source}\n")
            for link in links:
                f.write(f"  {link}\n")
            f.write("\n")


    print(f"\n{GREEN}✅ Scan complete! Results saved in {result_path}{RESET}")
