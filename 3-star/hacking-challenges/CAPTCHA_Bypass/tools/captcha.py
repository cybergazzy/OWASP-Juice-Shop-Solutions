import time
import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:3000"

# Optional: Add Authorization header if your target instance requires JWT tokens
HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer [PUT YOUR BEARER TOKEN HERE AND UNCOMMENT IF YOU NEED IT]"
}

def submit_single_feedback(index: int) -> bool:
    """Fetches a captcha, solves it, and submits a feedback entry."""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        captcha_res = session.get(f"{BASE_URL}/rest/captcha/")
        if captcha_res.status_code != 200:
            print(f"[{index}] Failed to fetch CAPTCHA (Status: {captcha_res.status_code})")
            return False

        captcha_data = captcha_res.json()
        captcha_id = captcha_data.get("captchaId")
        
        raw_answer = captcha_data.get("answer")
        if raw_answer is not None:
            captcha_answer = str(raw_answer)
        else:
            captcha_answer = str(eval(captcha_data.get("captcha", "0")))

        payload = {
            "captchaId": captcha_id,
            "captcha": captcha_answer,
            "comment": f"Cybergazzy was here",
            "rating": 5,
            # "UserId": 26  # Include if required for logged-in submissions
        }

        feedback_res = session.post(f"{BASE_URL}/api/Feedbacks/", json=payload)
        
        if feedback_res.status_code in (200, 201):
            print(f"[{index}] Successfully submitted feedback!")
            return True
        else:
            print(f"[{index}] Submission failed ({feedback_res.status_code}): {feedback_res.text}")
            return False

    except Exception as e:
        print(f"[{index}] Exception occurred: {e}")
        return False

def main():
    total_feedbacks = 12
    max_workers = 6
    print(f"Starting submission of {total_feedbacks} feedback requests...\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(submit_single_feedback, range(1, total_feedbacks + 1)))

    elapsed_time = time.time() - start_time
    successful = sum(1 for r in results if r)

    print("\n--- Summary ---")
    print(f"Successful: {successful}/{total_feedbacks}")
    print(f"Time Taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
