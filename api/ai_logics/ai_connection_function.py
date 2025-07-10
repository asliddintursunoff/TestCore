from google import genai
from google.genai import types
import time
from itertools import cycle
import asyncio
import threading
KEYS = ["AIzaSyDa7nRW0zK7L4XP8z31RHTFTmPIUEwk20g",
        "AIzaSyCaXqoBATI5HDLUyh3S0fGBTC-ibzk7TGs",
        "AIzaSyDR5Y29TWHDNMeohzJDGWGV0iVs4u4QSuY",
        "AIzaSyDJV-cwZ1CPHbpaigUt5ozHSZKmWgHt_Is",
        "AIzaSyDFZBX2AcItFgZ4-LylaebqTED5e0hAOnE",
        "AIzaSyAasuwKasTrJTEY-OcMhklDwRQWuwSDATY",
        "AIzaSyBe5ZRKHwFO9HbHIRz6rtQ4lUj9KafC4Bs",
        "AIzaSyC8-ueO52yuKGKwqgUYaowzF8K8YBmjO_A",
        "AIzaSyCG4SlAtFmrpBICLRsb-thlBvdl0hbZ_1g",
        "AIzaSyBE6dwMvxJ3LHjQRhuGTZ3DDab3lseR1yg",
        "AIzaSyBBWQ2y5h70e5010MwhCEPLqagKSVGHNm8",
        "AIzaSyBQ1y7VMpvrHHp55nRO5o5WbKfvkzJ6Jfs",
        "AIzaSyAPbT2X6UtDE3kd2p1QpfrYdXrgdBTvV_o",
        "AIzaSyArAzN0GHzrQOITsZDcwpt8Bh3Nl49fCaY",
        "AIzaSyAXPdsZwi_b1AZ3j6gnYYi2fQeCntZHOyg",
        "AIzaSyDCYUkRQUwlA8Pj0KUdjFDOg_ybZnY51bQ",
        "AIzaSyC94Tq3TbP5xtE-59E01w8cbLF2TLsQZuc"
        ]



# key_index = 0
# last_cycle_time = 0
# blacklisted_keys = set()
# used_keys_this_cycle = set()
# lock = threading.Lock()

# def get_api_key():
#     global key_index, last_cycle_time, blacklisted_keys, used_keys_this_cycle

#     with lock:
#         available_keys = [k for k in KEYS if k not in blacklisted_keys]

#         if not available_keys:
#             print("[ERROR] All API keys are blacklisted. Waiting 60 seconds...")
#             #time.sleep(60)
#             blacklisted_keys.clear()
#             used_keys_this_cycle.clear()
#             key_index = 0
#             available_keys = KEYS[:]

#         # Reset cycle if all keys used once
#         if len(used_keys_this_cycle) == len(KEYS):
#             now = time.time()
#             if now - last_cycle_time < 60:
#                 wait_time = 60 - (now - last_cycle_time)
#                 print(f"[WAIT] All API keys used once. Waiting {wait_time:.2f} seconds...")
#                 time.sleep(wait_time)
#             print("[RESET] Starting new API key cycle...")
#             used_keys_this_cycle.clear()
#             key_index = 0
#             last_cycle_time = time.time()

#         if key_index >= len(available_keys):
#             key_index = 0

#         key = available_keys[key_index]
#         key_index += 1
#         used_keys_this_cycle.add(key)

#         return key
key_index = 0
lock = threading.Lock()

def number_of_all_api_tokens():
    return len(KEYS)

def get_api_key():
    global key_index

    with lock:
        if not KEYS:
            raise Exception("No API keys available.")

        key = KEYS[key_index]
        key_index = (key_index + 1) % len(KEYS)
        return key

def generate(question):
    api = get_api_key()
    print(f"[KEY USED] {api}")

    try:
        start = time.time()
        client = genai.Client(api_key=api)

        model = "gemini-2.5-flash"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=question)],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=-1),
            response_mime_type="text/plain",
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        end = time.time()
        print(f"Execution time: {end - start:.4f} seconds")
        return response.text

    except Exception as e:
        # Detect 429 error from exception message
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            print(f"[BLACKLIST] API key {api} is exhausted. Blacklisting.")
           
        #print(f"[ERROR] API key: {api}")

        raise



async def generate_async(question):
    while True:
        try:
            return await asyncio.to_thread(generate, question)
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                #print("[RETRY] Quota error, retrying with next key...")
                continue  # Try again with a new key
            else:
                print(f"[FATAL ERROR] {e}")
                continue  # Re-raise for unexpected errors

