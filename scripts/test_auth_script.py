import httpx

def get_login_url(base_url):
    try:
        response = httpx.get(f"{base_url}/v1/auth/login")
        if response.status_code == 200:
            return response.url
        else:
            print(f"Error: Received status code {response.status_code} from login endpoint")
            return None
    except Exception as e:
        print(f"Error: Could not connect to the login endpoint. Details: {e}")
        return None

def test_callback_url(callback_url):
    try:
        response = httpx.get(callback_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code} from callback endpoint")
            return None
    except Exception as e:
        print(f"Error: Could not connect to the callback endpoint. Details: {e}")
        return None

def main():
    base_url = "http://localhost:8000/api"  # Replace with your FastAPI server URL

    # Step 1: Get Login URL
    github_auth_url = get_login_url(base_url)
    if github_auth_url:
        print("GitHub App Installation URL:", github_auth_url)
        print("Please complete the installation process in the browser and paste the callback URL here.")
        callback_url = input("Enter the callback URL: ")

        # Step 2: Test Callback URL
        callback_response = test_callback_url(callback_url)
        if callback_response:
            print("Callback Response:", callback_response)
        else:
            print("Failed to get a valid response from the callback URL.")
    else:
        print("Failed to retrieve the GitHub App installation URL.")

if __name__ == "__main__":
    main()
